import numpy as np
import scipy.ndimage as ndi
from scipy.optimize import linear_sum_assignment
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import os
import json

def get_portrait_dots(image_path="github_avatar.png", width=300, height=340):
    """
    Crop head + shoulders, apply autocontrast(cutoff=1), contrast 1.3x, unsharp mask,
    apply segmentation mask to isolate subject, and Floyd-Steinberg dither (serpentine).
    """
    img = Image.open(image_path).convert('RGB')
    
    # Clean head + shoulders crop from avatar (460x460)
    # y from 40 to 450, x from 0 to 362 -> aspect ratio 300:340
    crop_w = int(410 * 300.0 / 340.0) # 361
    crop_img = img.crop((0, 45, crop_w, 455)).resize((width, height), Image.Resampling.LANCZOS)
    
    # Preprocessing
    gray = ImageOps.grayscale(crop_img)
    gray = ImageOps.autocontrast(gray, cutoff=1)
    gray = ImageEnhance.Contrast(gray).enhance(1.3)
    gray = gray.filter(ImageFilter.UnsharpMask(radius=3, percent=140))
    
    gray_arr = np.array(gray).astype(np.float64)
    
    # Precise subject segmentation mask for 300x340
    h, w = height, width
    right_b = np.zeros(h)
    left_b = np.zeros(h)
    
    for y in range(h):
        if y < 15:
            left_b[y] = 300
            right_b[y] = 0
        elif y < 45:
            left_b[y] = max(18.0, 32.0 - (y - 15) * 0.4)
            right_b[y] = 85.0 + (y - 15) * 1.3
        elif y < 85:
            left_b[y] = 20.0
            right_b[y] = 124.0
        elif y < 105:
            left_b[y] = 20.0
            right_b[y] = 135.0  # Sunglasses edge
        elif y < 120:
            left_b[y] = 20.0
            right_b[y] = 128.0  # Far cheek
        elif y < 132:
            left_b[y] = 20.0
            right_b[y] = 126.0  # Lips
        elif y < 145:
            left_b[y] = 20.0
            right_b[y] = 123.0  # Chin
        elif y < 175:
            left_b[y] = 20.0
            right_b[y] = 112.0  # Neck
        elif y < 195:
            left_b[y] = 18.0
            right_b[y] = 112.0 + (y - 175) * 1.0  # Collar & shoulder
        elif y < 250:
            left_b[y] = 15.0
            right_b[y] = 132.0 + (y - 195) * 0.8  # Chest
        else:
            left_b[y] = 10.0
            right_b[y] = 176.0 + (y - 250) * 0.7  # Sweater torso & chair arm
            
    YY, XX = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')
    mask = (XX >= left_b[:, None]) & (XX <= right_b[:, None])
    
    # Invert for dark mode: lit areas get dots
    # Invert=False for light mode: dark parts get dots
    def dither(invert, apply_mask):
        buf = gray_arr.copy() if invert else (255.0 - gray_arr.copy())
        out = np.zeros((h, w), dtype=np.uint8)
        
        for y in range(h):
            if y % 2 == 0:
                x_range = range(w)
                direction = 1
            else:
                x_range = range(w - 1, -1, -1)
                direction = -1
                
            for x in x_range:
                if apply_mask and not mask[y, x]:
                    out[y, x] = 0
                    buf[y, x] = 0.0
                    continue
                    
                old_val = buf[y, x]
                new_val = 255.0 if old_val >= 128.0 else 0.0
                out[y, x] = 1 if new_val == 255.0 else 0
                err = old_val - new_val
                
                # Floyd-Steinberg error diffusion
                def add_err(ny, nx, weight):
                    if 0 <= ny < h and 0 <= nx < w:
                        if not apply_mask or mask[ny, nx]:
                            buf[ny, nx] += err * weight
                            
                add_err(y, x + direction, 7.0 / 16.0)
                add_err(y + 1, x - direction, 3.0 / 16.0)
                add_err(y + 1, x, 5.0 / 16.0)
                add_err(y + 1, x + direction, 1.0 / 16.0)
                
        return out
        
    dark_dither = dither(invert=True, apply_mask=True)
    light_dither = dither(invert=False, apply_mask=False)

    # Refresh source-of-truth .npy (the dither is deterministic from the photo,
    # but keep the arrays on disk as the canonical record alongside the logo dots).
    np.save("dark_dither.npy", dark_dither)
    np.save("light_dither.npy", light_dither)
    np.save("portrait_mask.npy", mask)

    return dark_dither, light_dither, mask

def dots_to_path_runs(dots):
    """
    Convert a list of (x, y) coordinates into compact SVG path runs:
    M x y h L v 1 h -L Z
    """
    if len(dots) == 0:
        return ""
    # Sort by y then x
    sorted_dots = sorted(dots, key=lambda p: (p[1], p[0]))
    
    runs = []
    curr_y = None
    curr_x_start = None
    curr_len = 0
    
    for x, y in sorted_dots:
        if curr_y is None:
            curr_y = y
            curr_x_start = x
            curr_len = 1
        elif y == curr_y and x == curr_x_start + curr_len:
            curr_len += 1
        else:
            runs.append((curr_x_start, curr_y, curr_len))
            curr_y = y
            curr_x_start = x
            curr_len = 1
    if curr_len > 0:
        runs.append((curr_x_start, curr_y, curr_len))
        
    path_cmds = []
    for x, y, l in runs:
        if l == 1:
            path_cmds.append(f"M{x} {y}h1v1h-1Z")
        else:
            path_cmds.append(f"M{x} {y}h{l}v1h-{l}Z")
    return "".join(path_cmds)

def compute_evenness_metric(groups_dots, num_bins=(8, 8), grid_shape=(340, 300)):
    """
    Total variation distance of spatial distribution across intro groups.
    Target: ~0.05 (uniform interleaved random scatter).
    """
    h, w = grid_shape
    all_dots = np.vstack(groups_dots)
    full_hist, _, _ = np.histogram2d(all_dots[:, 0], all_dots[:, 1], bins=num_bins, range=[[0, w], [0, h]])
    full_prob = full_hist / full_hist.sum()
    
    tv_dists = []
    for g_dots in groups_dots:
        if len(g_dots) == 0:
            continue
        g_hist, _, _ = np.histogram2d(g_dots[:, 0], g_dots[:, 1], bins=num_bins, range=[[0, w], [0, h]])
        g_prob = g_hist / g_hist.sum()
        tv = 0.5 * np.sum(np.abs(g_prob - full_prob))
        tv_dists.append(tv)
    return float(np.mean(tv_dists))

def compute_straight_boundary_metric(band_assignments, dots, grid_shape=(340, 300)):
    """
    Measures linearity of boundary edges between adjacent bands.
    Target: ~0.01 for organic noisy boundaries, ~0.17 for square grid.
    """
    h, w = grid_shape
    label_map = np.full((h, w), -1, dtype=np.int32)
    for (x, y), b in zip(dots, band_assignments):
        label_map[int(y), int(x)] = b
        
    h_diff = (label_map[:, 1:] != label_map[:, :-1]) & (label_map[:, 1:] != -1) & (label_map[:, :-1] != -1)
    v_diff = (label_map[1:, :] != label_map[:-1, :]) & (label_map[1:, :] != -1) & (label_map[:-1, :] != -1)
    
    total_boundary = h_diff.sum() + v_diff.sum()
    if total_boundary == 0:
        return 0.0
        
    h_runs = []
    for r in range(h_diff.shape[0]):
        row = h_diff[r]
        labeled_runs, num_runs = ndi.label(row)
        if num_runs > 0:
            run_lens = ndi.sum(row, labeled_runs, range(1, num_runs + 1))
            h_runs.extend(run_lens)
            
    long_runs_sum = sum(l for l in h_runs if l >= 5)
    return float(long_runs_sum / total_boundary)

def match_optimal_transport(pts_a, pts_b):
    """
    Find optimal transport permutation minimizing Euclidean distance sum.
    """
    cost_matrix = np.linalg.norm(pts_a[:, None, :] - pts_b[None, :, :], axis=2)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    return col_ind

def build_svg(is_dark=True):
    # Palette
    if is_dark:
        bg_color = "#0A101F"
        card_bg = "#0D1527"
        border_color = "rgba(34, 211, 238, 0.25)"
        title_color = "#94A3B8"
        chrome_color = "#22D3EE"
        chrome_dim = "rgba(34, 211, 238, 0.45)"
        text_label = "#94A3B8"
        text_dots = "rgba(100, 116, 139, 0.4)"
        text_val = "#E2E8F0"
        accent_color = "#10B981"
        portrait_color = "#A78BFA"
        pill_bg = "rgba(34, 211, 238, 0.12)"
    else:
        bg_color = "#F8FAFC"
        card_bg = "#FFFFFF"
        border_color = "rgba(8, 145, 178, 0.3)"
        title_color = "#475569"
        chrome_color = "#0891B2"
        chrome_dim = "rgba(8, 145, 178, 0.45)"
        text_label = "#64748B"
        text_dots = "rgba(148, 163, 184, 0.5)"
        text_val = "#0F172A"
        accent_color = "#059669"
        portrait_color = "#7C3AED"
        pill_bg = "rgba(8, 145, 178, 0.1)"
        
    print(f"Building {'dark' if is_dark else 'light'} banner...")
    
    # Load or generate dither
    dark_dither, light_dither, mask = get_portrait_dots("github_avatar.png", 300, 340)
    dither_map = dark_dither if is_dark else light_dither
    
    # Active dots in portrait
    ys, xs = np.where(dither_map == 1)
    portrait_dots = np.column_stack([xs, ys])
    num_portrait_dots = len(portrait_dots)
    print(f"Portrait dots count: {num_portrait_dots}")
    
    # 1. Intro grouping: 60 interleaved random groups
    np.random.seed(42)
    intro_perm = np.random.permutation(num_portrait_dots)
    num_intro_groups = 60
    intro_groups = []
    for g in range(num_intro_groups):
        g_indices = intro_perm[g::num_intro_groups]
        intro_groups.append(portrait_dots[g_indices])
        
    evenness = compute_evenness_metric(intro_groups)
    print(f"Intro evenness metric: {evenness:.4f} (target: ~0.05)")
    
    # 2. Loop drift grouping: ~94 drift bands with noise sigma=4
    # First logo is Python. Load Python 900 dots
    py_dots = np.load('py_dots_900.npy')
    li_dots = np.load('li_dots_900.npy')
    dk_dots = np.load('dk_dots_900.npy')
    
    py_centroid = np.mean(py_dots, axis=0) # [cx, cy]
    print(f"Python centroid: {py_centroid}")
    
    # Add noise sigma ~ 4 before grouping
    noise = np.random.normal(0, 4.0, portrait_dots.shape)
    noisy_coords = portrait_dots + noise
    
    # Drift vector towards py_centroid
    dists_to_py = np.linalg.norm(noisy_coords - py_centroid, axis=1)
    num_bands = 94
    quantiles = np.percentile(dists_to_py, np.linspace(0, 100, num_bands + 1))
    band_assignments = np.clip(np.digitize(dists_to_py, quantiles) - 1, 0, num_bands - 1)
    
    # NOTE: this run-length metric is confounded on sparse dither data + diagonal
    # band boundaries (a true square grid scores ~0.0, random noise ~0.3), so it does
    # NOT match the "~0.01 organic / ~0.17 grid" reading the design notes assumed.
    # The sigma=4 jitter is applied; the dissolve is verified in-browser, not by this number.
    straight_metric = compute_straight_boundary_metric(band_assignments, portrait_dots)
    print(f"Drift straight-boundary metric (confounded, informational only): {straight_metric:.4f}")
    
    # 3. Travellers optimal transport: Python -> Linux -> Docker
    # Match py -> li
    match_py_to_li = match_optimal_transport(py_dots, li_dots)
    matched_li = li_dots[match_py_to_li]
    
    # Match li -> dk
    match_li_to_dk = match_optimal_transport(matched_li, dk_dots)
    matched_dk = dk_dots[match_li_to_dk]
    
    # Now dot i has:
    # Python: py_dots[i]
    # Linux: matched_li[i]
    # Docker: matched_dk[i]
    
    # KeyTimes breakdown for 14.2s cycle:
    # 0s: portrait hold start (0.0)
    # 3.0s: portrait hold end / dissolve start (3.0 / 14.2 = 0.2113)
    # 4.3s: dissolve end / Python hold start (4.3 / 14.2 = 0.3028)
    # 6.3s: Python hold end / morph to Linux start (6.3 / 14.2 = 0.4437)
    # 7.6s: Linux hold start (7.6 / 14.2 = 0.5352)
    # 9.6s: Linux hold end / morph to Docker start (9.6 / 14.2 = 0.6761)
    # 10.9s: Docker hold start (10.9 / 14.2 = 0.7676)
    # 12.9s: Docker hold end / return to portrait start (12.9 / 14.2 = 0.9085)
    # 14.2s: cycle complete (1.0000)
    key_times = "0;0.2113;0.3028;0.4437;0.5352;0.6761;0.7676;0.9085;1"
    
    # SVG Dimensions
    W, H = 1180, 610
    
    # Portrait placement inside frame:
    # Frame is at x=32, y=60, w=396, h=518
    # Center 300x340 portrait inside frame:
    port_x = 32 + int((396 - 300) / 2) # 80
    port_y = 60 + 55 # 115
    
    svg_parts = []
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    svg_parts.append('<defs>')
    svg_parts.append('''
        <style>
            @keyframes pulse-live {
                0%, 100% { opacity: 1; transform: scale(1); }
                50% { opacity: 0.3; transform: scale(0.85); }
            }
            .live-dot {
                animation: pulse-live 1.6s ease-in-out infinite;
                transform-origin: 1060px 24px;
            }
            .mono {
                font-family: ui-monospace, "SF Mono", Monaco, Menlo, Consolas, "Liberation Mono", monospace;
            }
        </style>
    ''')
    svg_parts.append('</defs>')
    
    # Window Card Background & Border
    svg_parts.append(f'<rect width="{W}" height="{H}" rx="14" fill="{bg_color}"/>')
    svg_parts.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="13" fill="{card_bg}" stroke="{border_color}" stroke-width="1.5"/>')
    
    # Title Bar
    svg_parts.append(f'<line x1="0" y1="46" x2="{W}" y2="46" stroke="{border_color}" stroke-width="1"/>')
    # Terminal traffic lights
    svg_parts.append('<circle cx="26" cy="24" r="5.5" fill="#EF4444"/>')
    svg_parts.append('<circle cx="44" cy="24" r="5.5" fill="#F59E0B"/>')
    svg_parts.append('<circle cx="62" cy="24" r="5.5" fill="#10B981"/>')
    
    # Title
    svg_parts.append(f'<text x="{W//2}" y="29" text-anchor="middle" font-size="13" font-weight="600" fill="{title_color}" class="mono">profile.sh --live</text>')
    
    # Pill with handle
    svg_parts.append(f'<rect x="895" y="13" width="135" height="22" rx="11" fill="{pill_bg}" stroke="{chrome_color}" stroke-width="1"/>')
    svg_parts.append(f'<text x="962" y="28" text-anchor="middle" font-size="13" font-weight="600" fill="{chrome_color}" class="mono">@sailgaikwad</text>')
    
    # Pulsing red LIVE badge
    svg_parts.append('<g class="live-dot"><circle cx="1060" cy="24" r="4.5" fill="#EF4444"/></g>')
    svg_parts.append('<text x="1073" y="28" font-size="12" font-weight="700" fill="#EF4444" class="mono">LIVE</text>')
    
    # ================= LEFT PANEL: VISUAL.MAP =================
    frame_x, frame_y, frame_w, frame_h = 32, 62, 396, 516
    svg_parts.append(f'<rect x="{frame_x}" y="{frame_y}" width="{frame_w}" height="{frame_h}" rx="8" fill="none" stroke="{border_color}" stroke-width="1"/>')
    svg_parts.append(f'<rect x="{frame_x}" y="{frame_y}" width="{frame_w}" height="32" rx="8" fill="{pill_bg}"/>')
    svg_parts.append(f'<line x1="{frame_x}" y1="{frame_y+32}" x2="{frame_x+frame_w}" y2="{frame_y+32}" stroke="{border_color}" stroke-width="1"/>')
    svg_parts.append(f'<text x="{frame_x+16}" y="{frame_y+21}" font-size="13" font-weight="700" fill="{chrome_color}" class="mono">VISUAL.MAP</text>')
    svg_parts.append(f'<text x="{frame_x+frame_w-16}" y="{frame_y+21}" text-anchor="end" font-size="11" fill="{chrome_dim}" class="mono">300×340 · 1-BIT</text>')
    
    # Frame bottom HUD
    svg_parts.append(f'<line x1="{frame_x}" y1="{frame_y+frame_h-36}" x2="{frame_x+frame_w}" y2="{frame_y+frame_h-36}" stroke="{border_color}" stroke-width="1"/>')
    svg_parts.append(f'<text x="{frame_x+16}" y="{frame_y+frame_h-14}" font-size="11" font-weight="600" fill="{chrome_color}" class="mono">MORPH // PY → LINUX → DOCKER</text>')
    svg_parts.append(f'<text x="{frame_x+frame_w-16}" y="{frame_y+frame_h-14}" text-anchor="end" font-size="11" fill="{accent_color}" class="mono">SYNC OK</text>')
    
    # ------------------ PORTRAIT INTRO LAYER (Plays once for 3.2s) ------------------
    # Duplicate portrait layer (~180KB). 60 interleaved random groups fade in over ~2.0s
    svg_parts.append(f'<g transform="translate({port_x}, {port_y})">')
    # Entire intro group hides at 3.2s
    svg_parts.append('<set attributeName="visibility" to="hidden" begin="3.2s" fill="freeze"/>')
    
    for g_idx, g_dots in enumerate(intro_groups):
        path_data = dots_to_path_runs(g_dots)
        # Staggered fade in across ~2.0s: dots appear everywhere and thicken together
        t_start = (g_idx / 59.0) * 1.55
        svg_parts.append(f'<path d="{path_data}" fill="{portrait_color}" shape-rendering="crispEdges" opacity="0">')
        svg_parts.append(f'<animate attributeName="opacity" begin="{t_start:.3f}s" dur="0.45s" from="0" to="1" fill="freeze"/>')
        svg_parts.append('</path>')
    svg_parts.append('</g>')
    
    # ------------------ PORTRAIT LOOP LAYER (Indefinite loop starting at 3.2s) ------------------
    # 94 drift bands. On loop each band translates ~42% toward first logo's centroid while fading, then returns
    # Gated hidden until 3.2s so it does NOT mask the intro dissolve beneath it (base opacity would be 1 otherwise).
    svg_parts.append(f'<g transform="translate({port_x}, {port_y})" visibility="hidden">')
    svg_parts.append('<set attributeName="visibility" to="visible" begin="3.2s"/>')
    for b_idx in range(num_bands):
        b_dots = portrait_dots[band_assignments == b_idx]
        if len(b_dots) == 0:
            continue
        path_data = dots_to_path_runs(b_dots)
        
        # Calculate ~42% translation toward py_centroid
        b_centroid = np.mean(b_dots, axis=0)
        drift_vec = (py_centroid - b_centroid) * 0.42
        dx = round(float(drift_vec[0]), 1)
        dy = round(float(drift_vec[1]), 1)
        
        svg_parts.append(f'<g>')
        # Animate opacity: visible during portrait hold (0 to 3.0s), dissolves to 0 at 4.3s, holds 0, returns at 12.9s -> 14.2s
        svg_parts.append(f'<animate attributeName="opacity" dur="14.2s" begin="3.2s" repeatCount="indefinite" keyTimes="{key_times}" values="1;1;0;0;0;0;0;0;1"/>')
        # Animate translation
        svg_parts.append(f'<animateTransform attributeName="transform" type="translate" dur="14.2s" begin="3.2s" repeatCount="indefinite" keyTimes="{key_times}" values="0 0;0 0;{dx} {dy};{dx} {dy};{dx} {dy};{dx} {dy};{dx} {dy};{dx} {dy};0 0"/>')
        svg_parts.append(f'<path d="{path_data}" fill="{portrait_color}" shape-rendering="crispEdges"/>')
        svg_parts.append('</g>')
    svg_parts.append('</g>')
    
    # ------------------ TRAVELLERS LAYER (~900 dots morphing between logos) ------------------
    # Opacity keyframes 0;0;0;1;1;...;0 so hidden during portrait phase
    # Gated hidden until 3.2s so the 900 dots don't stack at the origin (base x/y=0) during the intro.
    svg_parts.append(f'<g transform="translate({port_x}, {port_y})" visibility="hidden">')
    svg_parts.append('<set attributeName="visibility" to="visible" begin="3.2s"/>')
    for i in range(len(py_dots)):
        x_py, y_py = round(float(py_dots[i, 0]), 1), round(float(py_dots[i, 1]), 1)
        x_li, y_li = round(float(matched_li[i, 0]), 1), round(float(matched_li[i, 1]), 1)
        x_dk, y_dk = round(float(matched_dk[i, 0]), 1), round(float(matched_dk[i, 1]), 1)
        
        # Values across the 14.2s cycle
        x_vals = f"{x_py};{x_py};{x_py};{x_py};{x_li};{x_li};{x_dk};{x_dk};{x_py}"
        y_vals = f"{y_py};{y_py};{y_py};{y_py};{y_li};{y_li};{y_dk};{y_dk};{y_py}"
        
        # Opacity: hidden (0) during portrait hold (0 to 3s), fades in during 3s..4.3s, holds 1 through all logos, fades out 12.9s..14.2s
        op_vals = "0;0;1;1;1;1;1;1;0"
        
        # Draw traveller as 2.2px crisp square dot
        svg_parts.append(f'<rect width="2.2" height="2.2" rx="0.5" fill="{portrait_color}">')
        svg_parts.append(f'<animate attributeName="x" dur="14.2s" begin="3.2s" repeatCount="indefinite" keyTimes="{key_times}" values="{x_vals}"/>')
        svg_parts.append(f'<animate attributeName="y" dur="14.2s" begin="3.2s" repeatCount="indefinite" keyTimes="{key_times}" values="{y_vals}"/>')
        svg_parts.append(f'<animate attributeName="opacity" dur="14.2s" begin="3.2s" repeatCount="indefinite" keyTimes="{key_times}" values="{op_vals}"/>')
        svg_parts.append('</rect>')
    svg_parts.append('</g>')
    
    # ================= RIGHT PANEL: SYSTEM.INFO =================
    sys_x = 448
    sys_w = W - sys_x - 32 # 700px width
    svg_parts.append(f'<rect x="{sys_x}" y="{frame_y}" width="{sys_w}" height="{frame_h}" rx="8" fill="none" stroke="{border_color}" stroke-width="1"/>')
    svg_parts.append(f'<rect x="{sys_x}" y="{frame_y}" width="{sys_w}" height="32" rx="8" fill="{pill_bg}"/>')
    svg_parts.append(f'<line x1="{sys_x}" y1="{frame_y+32}" x2="{sys_x+sys_w}" y2="{frame_y+32}" stroke="{border_color}" stroke-width="1"/>')
    svg_parts.append(f'<text x="{sys_x+16}" y="{frame_y+21}" font-size="13" font-weight="700" fill="{chrome_color}" class="mono">SYSTEM.INFO</text>')
    svg_parts.append(f'<text x="{sys_x+sys_w-16}" y="{frame_y+21}" text-anchor="end" font-size="11" fill="{chrome_dim}" class="mono">ID: SG-2026 // NODE-01</text>')
    
    # Rows definitions
    rows = [
        # General Info
        ("Subject", "Sail Gaikwad"),
        ("Role", "Full-Stack Dev | Cybersecurity Enthusiast"),
        ("Origin", "Kopargaon, Maharashtra, India"),
        ("Education", "B.Tech IT, Sanjivani College of Eng."),
        ("Status", "Building + Learning + Shipping"),
        ("ToolChain", "VS Code, Git, Docker, Linux, Android Studio"),
        # Core
        ("Core.Lang", "Python, Java, JS, TS, C, C++, Kotlin, SQL"),
        ("Core.Frontend", "React, Next.js, Vite, Tailwind CSS, HTML, CSS"),
        ("Core.Backend", "Node.js, Express.js, Django, REST APIs"),
        ("Core.Database", "PostgreSQL, Supabase, SQLite, Firebase"),
        ("Core.Infra", "Docker, Google Cloud, Linux, GitHub"),
        # Grid
        ("Grid.Mail", "sailgaikwad108@gmail.com"),
        ("Grid.Portfolio", "coming soon"),
        ("Grid.LinkedIn", "linkedin.com/in/sailgaikwad"),
        ("Grid.GitHub", "github.com/sailgaikwad"),
        ("Grid.Facebook", "facebook.com/sailgaikwad"),
    ]
    
    row_start_y = 118
    row_spacing = 23
    row_x_start = sys_x + 16
    row_x_end = sys_x + sys_w - 16
    available_width = row_x_end - row_x_start # 668px
    
    char_w = 8.42 # exact character width for font-size 14 monospace
    
    for idx, (label, val) in enumerate(rows):
        # Additional spacing before section groups
        extra_y = 0
        if idx >= 6:
            extra_y += 8
        if idx >= 11:
            extra_y += 8
            
        cur_y = row_start_y + idx * row_spacing + extra_y
        
        label_len = len(label)
        val_len = len(val)
        
        label_w = round(label_len * char_w, 1)
        val_w = round(val_len * char_w, 1)
        
        # Calculate dotted leader gap
        dots_x_start = row_x_start + label_w + 8
        val_x_start = row_x_end - val_w
        dots_w = val_x_start - dots_x_start - 8
        
        num_dots = max(3, int(dots_w / char_w))
        dots_str = "." * num_dots
        actual_dots_w = round(num_dots * char_w, 1)
        
        # Label
        label_fill = chrome_color if idx in [0, 6, 11] else text_label
        svg_parts.append(f'<text x="{row_x_start}" y="{cur_y}" font-size="14" font-weight="600" fill="{label_fill}" class="mono">{label}</text>')
        
        # Dotted leader
        svg_parts.append(f'<text x="{dots_x_start}" y="{cur_y}" font-size="14" fill="{text_dots}" class="mono">{dots_str}</text>')
        
        # Value locked with textLength and lengthAdjust="spacingAndGlyphs"
        val_fill = accent_color if idx == 4 else text_val
        svg_parts.append(f'<text x="{val_x_start}" y="{cur_y}" font-size="14" font-weight="500" fill="{val_fill}" class="mono" textLength="{val_w}" lengthAdjust="spacingAndGlyphs">{val}</text>')
        
    # Terminal prompt at bottom
    prompt_y = frame_y + frame_h - 18
    svg_parts.append(f'<line x1="{sys_x}" y1="{frame_y+frame_h-36}" x2="{sys_x+sys_w}" y2="{frame_y+frame_h-36}" stroke="{border_color}" stroke-width="1"/>')
    svg_parts.append(f'<text x="{sys_x+16}" y="{prompt_y}" font-size="12" font-weight="600" fill="{accent_color}" class="mono">guest@sailgaikwad:~$</text>')
    svg_parts.append(f'<text x="{sys_x+180}" y="{prompt_y}" font-size="12" fill="{text_label}" class="mono">curl -s https://api.github.com/users/sailgaikwad</text>')
    # Blinking cursor
    svg_parts.append(f'<rect x="{sys_x+515}" y="{prompt_y-11}" width="7" height="14" fill="{accent_color}">')
    svg_parts.append('<animate attributeName="opacity" dur="1s" values="1;0;1" repeatCount="indefinite"/>')
    svg_parts.append('</rect>')
    
    svg_parts.append('</svg>')
    
    svg_content = "\n".join(svg_parts)
    filename = "dark.svg" if is_dark else "light.svg"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    file_size_kb = os.path.getsize(filename) / 1024.0
    print(f"Generated {filename}: {file_size_kb:.1f} KB")
    return filename, file_size_kb, evenness, straight_metric

def main():
    dark_file, dark_kb, dark_even, dark_straight = build_svg(is_dark=True)
    light_file, light_kb, light_even, light_straight = build_svg(is_dark=False)
    
    print("\n--- BANNER BUILD SUMMARY ---")
    print(f"Dark mode banner:  {dark_file} ({dark_kb:.1f} KB)")
    print(f"Light mode banner: {light_file} ({light_kb:.1f} KB)")
    print(f"Intro evenness metric:          {dark_even:.4f} (interleaved-random by construction; ~0.05 ideal)")
    print(f"Drift straight-boundary metric: {dark_straight:.4f} (confounded on dither data - informational only)")

if __name__ == '__main__':
    main()
