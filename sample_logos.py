import numpy as np
from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright

def render_svg_to_mask(svg_path, width=300, height=340, padding=40):
    """
    Render SVG icon centered inside a 300x340 canvas using Playwright / Chromium,
    producing an exact 300x340 binary/alpha mask.
    """
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()
        
    # Scale SVG to fit within (width - 2*padding, height - 2*padding)
    target_box = min(width - 2 * padding, height - 2 * padding)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                width: {width}px;
                height: {height}px;
                background: #000000;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
            }}
            svg {{
                width: {target_box}px;
                height: {target_box}px;
                fill: #ffffff;
            }}
        </style>
    </head>
    <body>
        {svg_content}
    </body>
    </html>
    """
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        page.set_content(html)
        screenshot = page.screenshot()
        browser.close()
        
    import io
    img = Image.open(io.BytesIO(screenshot)).convert('L')
    return np.array(img)

def sample_900_dots(mask_arr, num_dots=900):
    """
    Sample exactly `num_dots` points uniformly from the mask foreground
    using blue-noise / farthest-point / rejection sampling for clean dot spacing.
    """
    # Active pixels in mask (threshold > 100)
    ys, xs = np.where(mask_arr > 100)
    total_active = len(ys)
    if total_active < num_dots:
        raise ValueError(f"Mask only has {total_active} active pixels, cannot sample {num_dots}!")
        
    candidates = np.column_stack([xs, ys]).astype(np.float64)
    
    # We want 900 points with good spatial dispersion.
    # Start with random seed or k-means-like / farthest point sampling.
    np.random.seed(42)
    # Fast approach: pick 4000 random points and use k-means centroids, or farthest point
    # Since candidates is ~15000-30000 points, let's run MiniBatchKMeans or fast Lloyd relaxation
    indices = np.random.choice(len(candidates), num_dots, replace=False)
    pts = candidates[indices].copy()
    
    # Run 5 iterations of Lloyd relaxation snapped to nearest candidates
    # to achieve near-optimal blue-noise distribution:
    from scipy.spatial import cKDTree
    tree = cKDTree(candidates)
    
    for it in range(8):
        # Voronoi / nearest candidate
        _, nearest_idx = tree.query(pts)
        pts = candidates[nearest_idx]
        # Jitter slightly to escape local traps
        jitter = np.random.normal(0, 0.5, pts.shape)
        _, nearest_idx = tree.query(pts + jitter)
        pts = candidates[nearest_idx]
        
    # Ensure all points are unique
    unique_pts = np.unique(pts, axis=0)
    while len(unique_pts) < num_dots:
        missing = num_dots - len(unique_pts)
        extra_idx = np.random.choice(len(candidates), missing, replace=False)
        unique_pts = np.vstack([unique_pts, candidates[extra_idx]])
        unique_pts = np.unique(unique_pts, axis=0)
        
    return unique_pts[:num_dots]

def main():
    print("Rendering SVG icons to masks...")
    py_mask = render_svg_to_mask('python_icon.svg')
    li_mask = render_svg_to_mask('linux_icon.svg')
    dk_mask = render_svg_to_mask('docker_icon.svg')
    
    Image.fromarray(py_mask).save('py_rendered.png')
    Image.fromarray(li_mask).save('li_rendered.png')
    Image.fromarray(dk_mask).save('dk_rendered.png')
    
    print("Sampling 900 dots for each logo...")
    py_dots = sample_900_dots(py_mask, 900)
    li_dots = sample_900_dots(li_mask, 900)
    dk_dots = sample_900_dots(dk_mask, 900)
    
    print(f"Sampled: Python {len(py_dots)}, Linux {len(li_dots)}, Docker {len(dk_dots)}")
    
    # Save visualizations of sampled dots
    for name, dots in [('py', py_dots), ('li', li_dots), ('dk', dk_dots)]:
        vis = Image.new('RGB', (300, 340), (10, 16, 31))
        draw = ImageDraw.Draw(vis)
        for x, y in dots:
            draw.rectangle([x - 1, y - 1, x + 1, y + 1], fill=(167, 139, 250))
        vis.save(f'{name}_dots_900.png')
        np.save(f'{name}_dots_900.npy', dots)
        
    print("Visualizations saved!")

if __name__ == '__main__':
    main()
