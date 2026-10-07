import base64
import os
import zipfile

WORKSPACE_DIR = r"c:\Projects\git r"
ASSETS_DIR = os.path.join(WORKSPACE_DIR, "assets")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

ID_PNG_PATH = os.path.join(ASSETS_DIR, "id.png")
POINTING_PNG_PATH = os.path.join(ASSETS_DIR, "right_pointing.png")
FONT_MONO_PATH = os.path.join(FONTS_DIR, "jetbrains-mono.woff2")
FONT_SANS_PATH = os.path.join(FONTS_DIR, "space-grotesk.woff2")

def get_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

id_b64 = get_b64(ID_PNG_PATH)
pointing_b64 = get_b64(POINTING_PNG_PATH)
mono_b64 = get_b64(FONT_MONO_PATH)
sans_b64 = get_b64(FONT_SANS_PATH)

def make_font_css(prefix):
    return f"""<![CDATA[
    /* SIL Open Font License (OFL) - JetBrains Mono and Space Grotesk */
    @font-face {{
      font-family: '{prefix}Display';
      src: url('data:font/woff2;base64,{sans_b64}') format('woff2');
      font-weight: 600 700;
      font-display: swap;
    }}
    @font-face {{
      font-family: '{prefix}Mono';
      src: url('data:font/woff2;base64,{mono_b64}') format('woff2');
      font-weight: 400 600;
      font-display: swap;
    }}
    .{prefix}-sans {{ font-family: '{prefix}Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
    .{prefix}-mono {{ font-family: '{prefix}Mono', 'SF Mono', Consolas, Monaco, monospace; }}
    @media (prefers-reduced-motion: reduce) {{
      *, ::before, ::after {{
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
      }}
    }}
    ]]>"""

# =========================================================================
# 1. assets/hero.svg
# =========================================================================
def build_hero():
    prefix = "hero"
    css = make_font_css(prefix)
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 895 380" width="100%" height="100%">
  <defs>
    <style>
      {css}
      .cursor-blink {{ animation: {prefix}Blink 0.9s infinite step-start; }}
      @keyframes {prefix}Blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
      .float-card {{ animation: {prefix}Float 4s ease-in-out infinite; }}
      @keyframes {prefix}Float {{ 0%, 100% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-5px); }} }}
    </style>
    
    <!-- Background Dot Pattern -->
    <pattern id="{prefix}-dots" x="0" y="0" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.1" fill="#247bff" fill-opacity="0.14"/>
    </pattern>
    
    <!-- Border Gradient -->
    <linearGradient id="{prefix}-border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.8"/>
      <stop offset="45%" stop-color="#0e1b38" stop-opacity="0.2"/>
      <stop offset="70%" stop-color="#ff354f" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#247bff" stop-opacity="0.8"/>
    </linearGradient>

    <!-- Card Rim Glow -->
    <linearGradient id="{prefix}-portrait-rim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#247bff"/>
      <stop offset="50%" stop-color="#141f36"/>
      <stop offset="100%" stop-color="#ff354f"/>
    </linearGradient>

    <!-- Text Name Clip for Rising Reveal -->
    <clipPath id="{prefix}-name-clip">
      <rect x="-5" y="65" width="580" height="74" rx="4"/>
    </clipPath>
    
    <!-- Portrait Inner Clip -->
    <clipPath id="{prefix}-portrait-clip">
      <rect x="600" y="38" width="255" height="304" rx="20"/>
    </clipPath>
  </defs>

  <!-- Base Canvas -->
  <rect width="895" height="380" rx="18" fill="#070b16"/>
  <rect width="895" height="380" rx="18" fill="url(#{prefix}-dots)"/>
  <rect x="1" y="1" width="893" height="378" rx="17" fill="none" stroke="url(#{prefix}-border-grad)" stroke-width="1.5"/>

  <!-- Left Content Column -->
  <g transform="translate(45, 0)">
    <!-- Terminal Prompt / Typed Greeting -->
    <g transform="translate(0, 48)">
      <rect x="0" y="-18" width="250" height="26" rx="6" fill="#0d1527" stroke="#247bff" stroke-width="1" stroke-opacity="0.35"/>
      <circle cx="14" cy="-5" r="4" fill="#ff354f"/>
      <circle cx="26" cy="-5" r="4" fill="#facc15"/>
      <circle cx="38" cy="-5" r="4" fill="#10b981"/>
      <text x="52" y="-1" class="{prefix}-mono" font-size="11.5" font-weight="600" fill="#247bff" letter-spacing="0.5">DEV.IDENTITY // ONLINE</text>
    </g>

    <!-- Rising Name Reveal inside Mask -->
    <g clip-path="url(#{prefix}-name-clip)">
      <g>
        <animateTransform attributeName="transform" type="translate" from="0,75" to="0,0" dur="0.8s" fill="freeze" calcMode="spline" keySplines="0.16 1 0.3 1" keyTimes="0;1"/>
        <text x="0" y="124" class="{prefix}-sans" font-size="52" font-weight="700" fill="#f0f4fc" letter-spacing="-0.5">SAIL GAIKWAD</text>
      </g>
    </g>

    <!-- Four Cycling Roles (SMIL 12s loop) -->
    <g transform="translate(2, 168)">
      <!-- Role 1 -->
      <g>
        <animate attributeName="opacity" values="1;1;0;0;0;0;0;1" keyTimes="0;0.22;0.25;0.72;0.75;0.95;0.98;1" dur="12s" repeatCount="indefinite"/>
        <text x="0" y="0" class="{prefix}-mono" font-size="19" font-weight="600" fill="#247bff">
          &gt; <tspan fill="#f0f4fc">Cybersecurity Researcher</tspan>
        </text>
      </g>
      <!-- Role 2 -->
      <g opacity="0">
        <animate attributeName="opacity" values="0;0;1;1;0;0;0;0" keyTimes="0;0.22;0.25;0.47;0.50;0.95;0.98;1" dur="12s" repeatCount="indefinite"/>
        <text x="0" y="0" class="{prefix}-mono" font-size="19" font-weight="600" fill="#ff354f">
          &gt; <tspan fill="#f0f4fc">AI Security &amp; LLM Defense</tspan>
        </text>
      </g>
      <!-- Role 3 -->
      <g opacity="0">
        <animate attributeName="opacity" values="0;0;0;0;1;1;0;0" keyTimes="0;0.47;0.50;0.72;0.75;0.95;0.98;1" dur="12s" repeatCount="indefinite"/>
        <text x="0" y="0" class="{prefix}-mono" font-size="19" font-weight="600" fill="#247bff">
          &gt; <tspan fill="#f0f4fc">Full-Stack Engineer</tspan>
        </text>
      </g>
      <!-- Role 4 -->
      <g opacity="0">
        <animate attributeName="opacity" values="0;0;0;0;0;0;1;1" keyTimes="0;0.72;0.75;0.95;0.98;1;1;1" dur="12s" repeatCount="indefinite"/>
        <text x="0" y="0" class="{prefix}-mono" font-size="19" font-weight="600" fill="#ff354f">
          &gt; <tspan fill="#f0f4fc">Autonomous Systems Builder</tspan>
        </text>
      </g>
      <!-- Cursor -->
      <rect x="350" y="-17" width="9" height="21" rx="2" fill="#247bff" class="cursor-blink"/>
    </g>

    <!-- One-line pitch -->
    <text x="2" y="212" class="{prefix}-sans" font-size="15" fill="#94a3b8" letter-spacing="0.2">
      Architecting secure AI systems, autonomous defense &amp; robust software.
    </text>

    <!-- Location & Metadata Pills Row -->
    <g transform="translate(2, 252)">
      <!-- Pill 1: Location -->
      <g>
        <rect x="0" y="0" width="180" height="34" rx="8" fill="#0d1424" stroke="#247bff" stroke-width="1" stroke-opacity="0.3"/>
        <text x="14" y="22" class="{prefix}-sans" font-size="13" fill="#cbd5e1">📍 Maharashtra, India</text>
      </g>
      <!-- Pill 2: Status -->
      <g transform="translate(192, 0)">
        <rect x="0" y="0" width="168" height="34" rx="8" fill="#0d1424" stroke="#10b981" stroke-width="1" stroke-opacity="0.3"/>
        <circle cx="16" cy="17" r="4.5" fill="#10b981">
          <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>
        </circle>
        <text x="28" y="22" class="{prefix}-sans" font-size="13" fill="#10b981">Open to Collabs</text>
      </g>
      <!-- Pill 3: Repos -->
      <g transform="translate(372, 0)">
        <rect x="0" y="0" width="140" height="34" rx="8" fill="#0d1424" stroke="#ff354f" stroke-width="1" stroke-opacity="0.3"/>
        <text x="14" y="22" class="{prefix}-mono" font-size="12" fill="#cbd5e1">⚡ 8+ Repos</text>
      </g>
    </g>

    <!-- Quick Tech Ribbon -->
    <g transform="translate(2, 316)">
      <text x="0" y="16" class="{prefix}-mono" font-size="11" fill="#64748b" letter-spacing="0.8">CORE FOCUS // PYTHON · DOCKER · LINUX · AI SECURITY · REACT</text>
    </g>
  </g>

  <!-- Right Side Portrait Card (Floating Card) -->
  <g class="float-card">
    <!-- Card Frame -->
    <rect x="600" y="38" width="255" height="304" rx="20" fill="#0b1122"/>
    <rect x="600" y="38" width="255" height="304" rx="20" fill="url(#{prefix}-dots)"/>
    
    <!-- Base64 Inlined Character Image -->
    <image href="data:image/png;base64,{id_b64}" x="575" y="20" width="305" height="305" clip-path="url(#{prefix}-portrait-clip)" preserveAspectRatio="xMidYMid meet"/>
    
    <!-- Outer Hairline Gradient Border -->
    <rect x="600" y="38" width="255" height="304" rx="20" fill="none" stroke="url(#{prefix}-portrait-rim)" stroke-width="2"/>
    
    <!-- Bottom Verified Badge on Portrait -->
    <g transform="translate(618, 308)">
      <rect x="0" y="0" width="218" height="24" rx="6" fill="#070b16" fill-opacity="0.9" stroke="#247bff" stroke-width="1" stroke-opacity="0.6"/>
      <circle cx="12" cy="12" r="3.5" fill="#247bff">
        <animate attributeName="opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite"/>
      </circle>
      <text x="24" y="16.5" class="{prefix}-mono" font-size="10" font-weight="600" fill="#f0f4fc" letter-spacing="0.6">SAIL // IDENTITY VERIFIED</text>
    </g>
  </g>
</svg>"""
    return svg

# =========================================================================
# 2. assets/about-life.svg
# =========================================================================
def build_about_life():
    prefix = "about"
    css = make_font_css(prefix)
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 895 410" width="100%" height="100%">
  <defs>
    <style>
      {css}
    </style>
    
    <pattern id="{prefix}-dots" x="0" y="0" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.1" fill="#247bff" fill-opacity="0.14"/>
    </pattern>

    <linearGradient id="{prefix}-border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.7"/>
      <stop offset="50%" stop-color="#0e1b38" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.6"/>
    </linearGradient>

    <linearGradient id="{prefix}-card-rim" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.6"/>
    </linearGradient>
  </defs>

  <!-- Base Canvas -->
  <rect width="895" height="410" rx="18" fill="#070b16"/>
  <rect width="895" height="410" rx="18" fill="url(#{prefix}-dots)"/>
  <rect x="1" y="1" width="893" height="408" rx="17" fill="none" stroke="url(#{prefix}-border-grad)" stroke-width="1.5"/>

  <!-- Left Column: Core Capabilities -->
  <g transform="translate(42, 36)">
    <!-- Column Header -->
    <g>
      <rect x="0" y="0" width="190" height="24" rx="6" fill="#0d1527" stroke="#247bff" stroke-width="1" stroke-opacity="0.4"/>
      <text x="10" y="16" class="{prefix}-mono" font-size="11" font-weight="600" fill="#247bff" letter-spacing="0.5">CAPABILITIES &amp; PILLARS</text>
    </g>
    <text x="0" y="52" class="{prefix}-sans" font-size="24" font-weight="700" fill="#f0f4fc">Engineering Mindset</text>
    <text x="0" y="74" class="{prefix}-sans" font-size="13" fill="#94a3b8">Specialized focus areas combining deep security with modern engineering.</text>

    <!-- Capability Cards -->
    <!-- Card 1 -->
    <g transform="translate(0, 96)">
      <rect x="0" y="0" width="375" height="74" rx="12" fill="#0b1122" stroke="#247bff" stroke-width="1" stroke-opacity="0.35"/>
      <rect x="14" y="14" width="32" height="32" rx="8" fill="#141f36"/>
      <text x="30" y="35" class="{prefix}-mono" font-size="14" fill="#247bff" text-anchor="middle" font-weight="700">01</text>
      <text x="56" y="28" class="{prefix}-sans" font-size="14" font-weight="700" fill="#f0f4fc">AI Security &amp; LLM Defense</text>
      <text x="56" y="48" class="{prefix}-sans" font-size="12" fill="#94a3b8">Adversarial testing, prompt hardening &amp; guardrails.</text>
    </g>

    <!-- Card 2 -->
    <g transform="translate(0, 180)">
      <rect x="0" y="0" width="375" height="74" rx="12" fill="#0b1122" stroke="#ff354f" stroke-width="1" stroke-opacity="0.35"/>
      <rect x="14" y="14" width="32" height="32" rx="8" fill="#2b141c"/>
      <text x="30" y="35" class="{prefix}-mono" font-size="14" fill="#ff354f" text-anchor="middle" font-weight="700">02</text>
      <text x="56" y="28" class="{prefix}-sans" font-size="14" font-weight="700" fill="#f0f4fc">Systems &amp; Cloud Infrastructure</text>
      <text x="56" y="48" class="{prefix}-sans" font-size="12" fill="#94a3b8">Linux kernel tools, Docker containerization &amp; cloud CSPs.</text>
    </g>

    <!-- Card 3 -->
    <g transform="translate(0, 264)">
      <rect x="0" y="0" width="375" height="74" rx="12" fill="#0b1122" stroke="#247bff" stroke-width="1" stroke-opacity="0.35"/>
      <rect x="14" y="14" width="32" height="32" rx="8" fill="#141f36"/>
      <text x="30" y="35" class="{prefix}-mono" font-size="14" fill="#247bff" text-anchor="middle" font-weight="700">03</text>
      <text x="56" y="28" class="{prefix}-sans" font-size="14" font-weight="700" fill="#f0f4fc">Defensive Full-Stack Tooling</text>
      <text x="56" y="48" class="{prefix}-sans" font-size="12" fill="#94a3b8">Python, Java &amp; JS for performant, robust platforms.</text>
    </g>
  </g>

  <!-- Right Column: 3-Slide Carousel Changing Every 4s -->
  <g transform="translate(455, 36)">
    <!-- Column Header -->
    <g>
      <rect x="0" y="0" width="220" height="24" rx="6" fill="#0d1527" stroke="#ff354f" stroke-width="1" stroke-opacity="0.4"/>
      <text x="10" y="16" class="{prefix}-mono" font-size="11" font-weight="600" fill="#ff354f" letter-spacing="0.5">INTERESTS &amp; PASSIONS // LIVE</text>
    </g>
    <text x="0" y="52" class="{prefix}-sans" font-size="24" font-weight="700" fill="#f0f4fc">Beyond the Terminal</text>
    <text x="0" y="74" class="{prefix}-sans" font-size="13" fill="#94a3b8">Exploring deep tech, research frontiers &amp; craftsmanship.</text>

    <!-- Carousel Card Container -->
    <g transform="translate(0, 96)">
      <rect x="0" y="0" width="398" height="242" rx="16" fill="#0b1122" stroke="url(#{prefix}-card-rim)" stroke-width="1.2"/>
      
      <!-- Top 3 Segment Progress Bars (12s cycle, 4s per segment) -->
      <g transform="translate(18, 18)">
        <!-- Bar 1 Background & Active Fill -->
        <rect x="0" y="0" width="114" height="4" rx="2" fill="#1a253d"/>
        <rect x="0" y="0" width="0" height="4" rx="2" fill="#247bff">
          <animate attributeName="width" values="0;114;114;0" keyTimes="0;0.33;0.98;1" dur="12s" repeatCount="indefinite"/>
        </rect>
        
        <!-- Bar 2 Background & Active Fill -->
        <rect x="124" y="0" width="114" height="4" rx="2" fill="#1a253d"/>
        <rect x="124" y="0" width="0" height="4" rx="2" fill="#ff354f">
          <animate attributeName="width" values="0;0;114;114;0" keyTimes="0;0.33;0.66;0.98;1" dur="12s" repeatCount="indefinite"/>
        </rect>

        <!-- Bar 3 Background & Active Fill -->
        <rect x="248" y="0" width="114" height="4" rx="2" fill="#1a253d"/>
        <rect x="248" y="0" width="0" height="4" rx="2" fill="#247bff">
          <animate attributeName="width" values="0;0;114;0" keyTimes="0;0.66;0.98;1" dur="12s" repeatCount="indefinite"/>
        </rect>
      </g>

      <!-- Carousel Slides (12s total loop, 4s per slide) -->
      <!-- SLIDE 1 (0s - 4s) -->
      <g transform="translate(20, 44)">
        <animate attributeName="opacity" values="1;1;0;0;0;0;0;1" keyTimes="0;0.30;0.34;0.70;0.74;0.95;0.98;1" dur="12s" repeatCount="indefinite"/>
        <g transform="translate(0, 0)">
          <rect x="0" y="0" width="48" height="48" rx="12" fill="#141f36"/>
          <text x="24" y="32" font-size="22" text-anchor="middle">🛡️</text>
        </g>
        <text x="60" y="24" class="{prefix}-mono" font-size="11" fill="#247bff" font-weight="600">SLIDE 01 / 03</text>
        <text x="60" y="44" class="{prefix}-sans" font-size="17" font-weight="700" fill="#f0f4fc">Cybersecurity &amp; CTF Research</text>
        
        <text x="0" y="86" class="{prefix}-sans" font-size="13.5" fill="#cbd5e1">
          Deep-diving into exploit chains, network packets,
        </text>
        <text x="0" y="108" class="{prefix}-sans" font-size="13.5" fill="#cbd5e1">
          malware behavior and digital forensics analysis.
        </text>
        
        <!-- Tags -->
        <g transform="translate(0, 134)">
          <rect x="0" y="0" width="96" height="26" rx="6" fill="#141f36"/>
          <text x="48" y="17" class="{prefix}-mono" font-size="11" fill="#247bff" text-anchor="middle">#CTF_Pwn</text>
          
          <rect x="104" y="0" width="112" height="26" rx="6" fill="#141f36"/>
          <text x="160" y="17" class="{prefix}-mono" font-size="11" fill="#247bff" text-anchor="middle">#ThreatHunting</text>

          <rect x="224" y="0" width="108" height="26" rx="6" fill="#141f36"/>
          <text x="278" y="17" class="{prefix}-mono" font-size="11" fill="#247bff" text-anchor="middle">#Forensics</text>
        </g>
      </g>

      <!-- SLIDE 2 (4s - 8s) -->
      <g transform="translate(20, 44)" opacity="0">
        <animate attributeName="opacity" values="0;0;1;1;0;0;0;0" keyTimes="0;0.31;0.34;0.63;0.67;0.95;0.98;1" dur="12s" repeatCount="indefinite"/>
        <g transform="translate(0, 0)">
          <rect x="0" y="0" width="48" height="48" rx="12" fill="#2b141c"/>
          <text x="24" y="32" font-size="22" text-anchor="middle">🤖</text>
        </g>
        <text x="60" y="24" class="{prefix}-mono" font-size="11" fill="#ff354f" font-weight="600">SLIDE 02 / 03</text>
        <text x="60" y="44" class="{prefix}-sans" font-size="17" font-weight="700" fill="#f0f4fc">Autonomous AI &amp; LLM Defense</text>
        
        <text x="0" y="86" class="{prefix}-sans" font-size="13.5" fill="#cbd5e1">
          Benchmarking adversarial prompts, building resilient
        </text>
        <text x="0" y="108" class="{prefix}-sans" font-size="13.5" fill="#cbd5e1">
          multi-agent frameworks, and securing model pipelines.
        </text>
        
        <!-- Tags -->
        <g transform="translate(0, 134)">
          <rect x="0" y="0" width="106" height="26" rx="6" fill="#2b141c"/>
          <text x="53" y="17" class="{prefix}-mono" font-size="11" fill="#ff354f" text-anchor="middle">#LLM_Security</text>
          
          <rect x="114" y="0" width="112" height="26" rx="6" fill="#2b141c"/>
          <text x="170" y="17" class="{prefix}-mono" font-size="11" fill="#ff354f" text-anchor="middle">#AI_Agents</text>

          <rect x="234" y="0" width="112" height="26" rx="6" fill="#2b141c"/>
          <text x="290" y="17" class="{prefix}-mono" font-size="11" fill="#ff354f" text-anchor="middle">#Guardrails</text>
        </g>
      </g>

      <!-- SLIDE 3 (8s - 12s) -->
      <g transform="translate(20, 44)" opacity="0">
        <animate attributeName="opacity" values="0;0;0;0;1;1;0;0" keyTimes="0;0.64;0.67;0.96;0.99;1;1;1" dur="12s" repeatCount="indefinite"/>
        <g transform="translate(0, 0)">
          <rect x="0" y="0" width="48" height="48" rx="12" fill="#141f36"/>
          <text x="24" y="32" font-size="22" text-anchor="middle">💻</text>
        </g>
        <text x="60" y="24" class="{prefix}-mono" font-size="11" fill="#247bff" font-weight="600">SLIDE 03 / 03</text>
        <text x="60" y="44" class="{prefix}-sans" font-size="17" font-weight="700" fill="#f0f4fc">Software Craftsmanship &amp; OSS</text>
        
        <text x="0" y="86" class="{prefix}-sans" font-size="13.5" fill="#cbd5e1">
          Designing clean command-line tools, reactive web
        </text>
        <text x="0" y="108" class="{prefix}-sans" font-size="13.5" fill="#cbd5e1">
          architectures, and high-performance system backends.
        </text>
        
        <!-- Tags -->
        <g transform="translate(0, 134)">
          <rect x="0" y="0" width="94" height="26" rx="6" fill="#141f36"/>
          <text x="47" y="17" class="{prefix}-mono" font-size="11" fill="#247bff" text-anchor="middle">#OpenSource</text>
          
          <rect x="102" y="0" width="112" height="26" rx="6" fill="#141f36"/>
          <text x="158" y="17" class="{prefix}-mono" font-size="11" fill="#247bff" text-anchor="middle">#SystemDesign</text>

          <rect x="222" y="0" width="102" height="26" rx="6" fill="#141f36"/>
          <text x="273" y="17" class="{prefix}-mono" font-size="11" fill="#247bff" text-anchor="middle">#CleanCode</text>
        </g>
      </g>
    </g>
  </g>
</svg>"""
    return svg

# =========================================================================
# 3. assets/stack.svg
# =========================================================================
def build_stack():
    prefix = "stack"
    css = make_font_css(prefix)
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 895 480" width="100%" height="100%">
  <defs>
    <style>
      {css}
      .orbit-pulse {{ animation: {prefix}Pulse 5s ease-in-out infinite; }}
      @keyframes {prefix}Pulse {{ 0%, 100% {{ opacity: 0.4; }} 50% {{ opacity: 0.8; }} }}
    </style>
    
    <pattern id="{prefix}-dots" x="0" y="0" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.1" fill="#247bff" fill-opacity="0.14"/>
    </pattern>

    <linearGradient id="{prefix}-border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.75"/>
      <stop offset="50%" stop-color="#0e1b38" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.6"/>
    </linearGradient>

    <!-- Node Gradient Fill -->
    <linearGradient id="{prefix}-node-blue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#247bff"/>
      <stop offset="100%" stop-color="#0e3a8a"/>
    </linearGradient>
    <linearGradient id="{prefix}-node-crimson" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ff354f"/>
      <stop offset="100%" stop-color="#8a1122"/>
    </linearGradient>
  </defs>

  <!-- Base Canvas -->
  <rect width="895" height="480" rx="18" fill="#070b16"/>
  <rect width="895" height="480" rx="18" fill="url(#{prefix}-dots)"/>
  <rect x="1" y="1" width="893" height="478" rx="17" fill="none" stroke="url(#{prefix}-border-grad)" stroke-width="1.5"/>

  <!-- Top Title Badge -->
  <g transform="translate(42, 28)">
    <rect x="0" y="0" width="170" height="24" rx="6" fill="#0d1527" stroke="#247bff" stroke-width="1" stroke-opacity="0.4"/>
    <text x="10" y="16" class="{prefix}-mono" font-size="11" font-weight="600" fill="#247bff" letter-spacing="0.5">TECHNICAL ARSENAL</text>
    <text x="180" y="18" class="{prefix}-sans" font-size="20" font-weight="700" fill="#f0f4fc">Three Tilted Elliptical Orbits &amp; Core Stack</text>
  </g>

  <!-- ================= THREE TILTED ELLIPTICAL ORBITS ================= -->
  <!-- Centered at (447, 145), tilted -12 degrees -->
  <g transform="translate(447, 145)">
    <!-- Orbits Group Tilted -->
    <g transform="rotate(-12)">
      <!-- Outer Orbit (Radius 360, 92) -->
      <ellipse cx="0" cy="0" rx="360" ry="92" fill="none" stroke="#247bff" stroke-width="1.4" stroke-dasharray="6,6" opacity="0.45" class="orbit-pulse"/>
      
      <!-- Middle Orbit (Radius 250, 68) -->
      <ellipse cx="0" cy="0" rx="250" ry="68" fill="none" stroke="#ff354f" stroke-width="1.4" stroke-dasharray="8,5" opacity="0.5" class="orbit-pulse"/>
      
      <!-- Inner Orbit (Radius 140, 42) -->
      <ellipse cx="0" cy="0" rx="140" ry="42" fill="none" stroke="#247bff" stroke-width="1.4" stroke-dasharray="4,4" opacity="0.6"/>

      <!-- Center Core Hub -->
      <circle cx="0" cy="0" r="16" fill="#0b1122" stroke="#247bff" stroke-width="2"/>
      <circle cx="0" cy="0" r="7" fill="#ff354f">
        <animate attributeName="r" values="6;8;6" dur="2s" repeatCount="indefinite"/>
      </circle>
    </g>

    <!-- Correctly Labelled Tech Nodes Positioned Along Orbits -->
    <!-- Inner Orbit Nodes -->
    <!-- Node 1: Python -->
    <g transform="translate(-110, -28)">
      <rect x="-42" y="-14" width="84" height="28" rx="8" fill="#0b1122" stroke="#247bff" stroke-width="1.2"/>
      <circle cx="-26" cy="0" r="5" fill="#247bff"/>
      <text x="-14" y="4.5" class="{prefix}-mono" font-size="12" font-weight="600" fill="#f0f4fc">Python</text>
    </g>

    <!-- Node 2: Docker -->
    <g transform="translate(105, 30)">
      <rect x="-42" y="-14" width="84" height="28" rx="8" fill="#0b1122" stroke="#247bff" stroke-width="1.2"/>
      <circle cx="-26" cy="0" r="5" fill="#247bff"/>
      <text x="-14" y="4.5" class="{prefix}-mono" font-size="12" font-weight="600" fill="#f0f4fc">Docker</text>
    </g>

    <!-- Node 3: Linux -->
    <g transform="translate(20, -45)">
      <rect x="-38" y="-14" width="76" height="28" rx="8" fill="#0b1122" stroke="#ff354f" stroke-width="1.2"/>
      <circle cx="-24" cy="0" r="5" fill="#ff354f"/>
      <text x="-12" y="4.5" class="{prefix}-mono" font-size="12" font-weight="600" fill="#f0f4fc">Linux</text>
    </g>

    <!-- Middle Orbit Nodes -->
    <!-- Node 4: TypeScript -->
    <g transform="translate(-230, 20)">
      <rect x="-50" y="-14" width="100" height="28" rx="8" fill="#0b1122" stroke="#ff354f" stroke-width="1.2"/>
      <circle cx="-34" cy="0" r="5" fill="#ff354f"/>
      <text x="-22" y="4.5" class="{prefix}-mono" font-size="11.5" font-weight="600" fill="#f0f4fc">TypeScript</text>
    </g>

    <!-- Node 5: React -->
    <g transform="translate(225, -25)">
      <rect x="-38" y="-14" width="76" height="28" rx="8" fill="#0b1122" stroke="#247bff" stroke-width="1.2"/>
      <circle cx="-24" cy="0" r="5" fill="#247bff"/>
      <text x="-12" y="4.5" class="{prefix}-mono" font-size="12" font-weight="600" fill="#f0f4fc">React</text>
    </g>

    <!-- Node 6: Java -->
    <g transform="translate(-60, 56)">
      <rect x="-34" y="-14" width="68" height="28" rx="8" fill="#0b1122" stroke="#247bff" stroke-width="1.2"/>
      <circle cx="-20" cy="0" r="5" fill="#247bff"/>
      <text x="-8" y="4.5" class="{prefix}-mono" font-size="12" font-weight="600" fill="#f0f4fc">Java</text>
    </g>

    <!-- Outer Orbit Nodes -->
    <!-- Node 7: AI Defense -->
    <g transform="translate(-320, -45)">
      <rect x="-56" y="-14" width="112" height="28" rx="8" fill="#0b1122" stroke="#247bff" stroke-width="1.2"/>
      <circle cx="-40" cy="0" r="5" fill="#247bff"/>
      <text x="-28" y="4.5" class="{prefix}-mono" font-size="11.5" font-weight="600" fill="#f0f4fc">AI Defense</text>
    </g>

    <!-- Node 8: C / C++ -->
    <g transform="translate(325, 42)">
      <rect x="-38" y="-14" width="76" height="28" rx="8" fill="#0b1122" stroke="#ff354f" stroke-width="1.2"/>
      <circle cx="-24" cy="0" r="5" fill="#ff354f"/>
      <text x="-12" y="4.5" class="{prefix}-mono" font-size="12" font-weight="600" fill="#f0f4fc">C / C++</text>
    </g>

    <!-- Node 9: Cloud / CSP -->
    <g transform="translate(130, -78)">
      <rect x="-48" y="-14" width="96" height="28" rx="8" fill="#0b1122" stroke="#247bff" stroke-width="1.2"/>
      <circle cx="-32" cy="0" r="5" fill="#247bff"/>
      <text x="-20" y="4.5" class="{prefix}-mono" font-size="11.5" font-weight="600" fill="#f0f4fc">Cloud / CSP</text>
    </g>
  </g>

  <!-- ================= GROUPED STACK CHIPS ================= -->
  <g transform="translate(42, 265)">
    <!-- Row 1: Languages & Security -->
    <!-- Group 1: Languages -->
    <g>
      <rect x="0" y="0" width="395" height="88" rx="12" fill="#0b1122" stroke="#247bff" stroke-width="1" stroke-opacity="0.35"/>
      <text x="16" y="24" class="{prefix}-mono" font-size="11" font-weight="600" fill="#247bff" letter-spacing="0.6">// PROGRAMMING LANGUAGES</text>
      <!-- Chips -->
      <g transform="translate(16, 36)">
        <rect x="0" y="0" width="62" height="26" rx="6" fill="#141f36"/>
        <text x="31" y="17" class="{prefix}-sans" font-size="12" font-weight="600" fill="#cbd5e1" text-anchor="middle">Python</text>

        <rect x="70" y="0" width="84" height="26" rx="6" fill="#141f36"/>
        <text x="112" y="17" class="{prefix}-sans" font-size="12" font-weight="600" fill="#cbd5e1" text-anchor="middle">TypeScript</text>

        <rect x="162" y="0" width="84" height="26" rx="6" fill="#141f36"/>
        <text x="204" y="17" class="{prefix}-sans" font-size="12" font-weight="600" fill="#cbd5e1" text-anchor="middle">JavaScript</text>

        <rect x="254" y="0" width="50" height="26" rx="6" fill="#141f36"/>
        <text x="279" y="17" class="{prefix}-sans" font-size="12" font-weight="600" fill="#cbd5e1" text-anchor="middle">Java</text>

        <rect x="312" y="0" width="50" height="26" rx="6" fill="#141f36"/>
        <text x="337" y="17" class="{prefix}-sans" font-size="12" font-weight="600" fill="#cbd5e1" text-anchor="middle">C / C++</text>
      </g>
    </g>

    <!-- Group 2: Security & Defense -->
    <g transform="translate(416, 0)">
      <rect x="0" y="0" width="395" height="88" rx="12" fill="#0b1122" stroke="#ff354f" stroke-width="1" stroke-opacity="0.35"/>
      <text x="16" y="24" class="{prefix}-mono" font-size="11" font-weight="600" fill="#ff354f" letter-spacing="0.6">// CYBERSECURITY &amp; DEFENSE</text>
      <!-- Chips -->
      <g transform="translate(16, 36)">
        <rect x="0" y="0" width="116" height="26" rx="6" fill="#2b141c"/>
        <text x="58" y="17" class="{prefix}-sans" font-size="12" font-weight="600" fill="#fca5a5" text-anchor="middle">Digital Forensics</text>

        <rect x="124" y="0" width="102" height="26" rx="6" fill="#2b141c"/>
        <text x="175" y="17" class="{prefix}-sans" font-size="12" font-weight="600" fill="#fca5a5" text-anchor="middle">AI Guardrails</text>

        <rect x="234" y="0" width="128" height="26" rx="6" fill="#2b141c"/>
        <text x="298" y="17" class="{prefix}-sans" font-size="12" font-weight="600" fill="#fca5a5" text-anchor="middle">Adversarial Eval</text>
      </g>
    </g>

    <!-- Row 2: Systems/DevOps & Frameworks -->
    <!-- Group 3: Systems & DevOps -->
    <g transform="translate(0, 98)">
      <rect x="0" y="0" width="395" height="88" rx="12" fill="#0b1122" stroke="#ff354f" stroke-width="1" stroke-opacity="0.35"/>
      <text x="16" y="24" class="{prefix}-mono" font-size="11" font-weight="600" fill="#ff354f" letter-spacing="0.6">// SYSTEMS &amp; INFRASTRUCTURE</text>
      <!-- Chips -->
      <g transform="translate(16, 36)">
        <rect x="0" y="0" width="56" height="26" rx="6" fill="#141f36"/>
        <text x="28" y="17" class="{prefix}-sans" font-size="12" font-weight="600" fill="#cbd5e1" text-anchor="middle">Linux</text>

        <rect x="64" y="0" width="62" height="26" rx="6" fill="#141f36"/>
        <text x="95" y="17" class="{prefix}-sans" font-size="12" font-weight="600" fill="#cbd5e1" text-anchor="middle">Docker</text>

        <rect x="134" y="0" width="46" height="26" rx="6" fill="#141f36"/>
        <text x="157" y="17" class="{prefix}-sans" font-size="12" font-weight="600" fill="#cbd5e1" text-anchor="middle">Git</text>

        <rect x="188" y="0" width="94" height="26" rx="6" fill="#141f36"/>
        <text x="235" y="17" class="{prefix}-sans" font-size="12" font-weight="600" fill="#cbd5e1" text-anchor="middle">Cloud (CSP)</text>

        <rect x="290" y="0" width="74" height="26" rx="6" fill="#141f36"/>
        <text x="327" y="17" class="{prefix}-sans" font-size="12" font-weight="600" fill="#cbd5e1" text-anchor="middle">Wireshark</text>
      </g>
    </g>

    <!-- Group 4: Frameworks & Web -->
    <g transform="translate(416, 98)">
      <rect x="0" y="0" width="395" height="88" rx="12" fill="#0b1122" stroke="#247bff" stroke-width="1" stroke-opacity="0.35"/>
      <text x="16" y="24" class="{prefix}-mono" font-size="11" font-weight="600" fill="#247bff" letter-spacing="0.6">// FRAMEWORKS &amp; DATABASES</text>
      <!-- Chips -->
      <g transform="translate(16, 36)">
        <rect x="0" y="0" width="56" height="26" rx="6" fill="#141f36"/>
        <text x="28" y="17" class="{prefix}-sans" font-size="12" font-weight="600" fill="#cbd5e1" text-anchor="middle">React</text>

        <rect x="64" y="0" width="66" height="26" rx="6" fill="#141f36"/>
        <text x="97" y="17" class="{prefix}-sans" font-size="12" font-weight="600" fill="#cbd5e1" text-anchor="middle">Node.js</text>

        <rect x="138" y="0" width="62" height="26" rx="6" fill="#141f36"/>
        <text x="169" y="17" class="{prefix}-sans" font-size="12" font-weight="600" fill="#cbd5e1" text-anchor="middle">FastAPI</text>

        <rect x="208" y="0" width="86" height="26" rx="6" fill="#141f36"/>
        <text x="251" y="17" class="{prefix}-sans" font-size="12" font-weight="600" fill="#cbd5e1" text-anchor="middle">PostgreSQL</text>

        <rect x="302" y="0" width="60" height="26" rx="6" fill="#141f36"/>
        <text x="332" y="17" class="{prefix}-sans" font-size="12" font-weight="600" fill="#cbd5e1" text-anchor="middle">SQLite</text>
      </g>
    </g>
  </g>
</svg>"""
    return svg

# =========================================================================
# 4. assets/id-dashboard.svg
# =========================================================================
def build_id_dashboard():
    prefix = "iddash"
    css = make_font_css(prefix)
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 895 520" width="100%" height="100%">
  <defs>
    <style>
      {css}
    </style>
    
    <pattern id="{prefix}-dots" x="0" y="0" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.1" fill="#247bff" fill-opacity="0.14"/>
    </pattern>

    <linearGradient id="{prefix}-border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.75"/>
      <stop offset="50%" stop-color="#0e1b38" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.6"/>
    </linearGradient>

    <!-- Metal Clasp Gradients -->
    <linearGradient id="{prefix}-metal-sheen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#475569"/>
      <stop offset="35%" stop-color="#cbd5e1"/>
      <stop offset="65%" stop-color="#94a3b8"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>

    <!-- Card Rim Gradient -->
    <linearGradient id="{prefix}-card-rim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#247bff"/>
      <stop offset="40%" stop-color="#141f36"/>
      <stop offset="100%" stop-color="#ff354f"/>
    </linearGradient>

    <!-- Foil Light Sweep Gradient -->
    <linearGradient id="{prefix}-foil-sweep" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="45%" stop-color="#247bff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.18"/>
      <stop offset="55%" stop-color="#ff354f" stop-opacity="0"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
      <animate attributeName="x1" values="-150%; 250%" dur="5.5s" repeatCount="indefinite"/>
    </linearGradient>

    <!-- Portrait Clip inside Badge -->
    <clipPath id="{prefix}-photo-clip">
      <rect x="185" y="160" width="140" height="155" rx="14"/>
    </clipPath>
  </defs>

  <!-- Base Canvas Background -->
  <rect width="895" height="520" rx="18" fill="#070b16"/>
  <rect width="895" height="520" rx="18" fill="url(#{prefix}-dots)"/>
  <rect x="1" y="1" width="893" height="518" rx="17" fill="none" stroke="url(#{prefix}-border-grad)" stroke-width="1.5"/>

  <!-- Top Fixed Lanyard Strap entering from top (x=447, y=0 to y=65) -->
  <g>
    <!-- Strap Webbing -->
    <rect x="432" y="0" width="32" height="65" fill="#0d1527"/>
    <line x1="432" y1="0" x2="432" y2="65" stroke="#247bff" stroke-width="2"/>
    <line x1="464" y1="0" x2="464" y2="65" stroke="#ff354f" stroke-width="2"/>
    <line x1="448" y1="0" x2="448" y2="65" stroke="#247bff" stroke-width="1" stroke-dasharray="3,3"/>
  </g>

  <!-- ================= DAMPED PENDULUM SWING BADGE ================= -->
  <!-- Pivot point at clasp: (447, 72) -->
  <!-- Initial drop & damped settle, then gentle continuous +/-1.7-degree swing -->
  <g id="{prefix}-pendulum">
    <animateTransform attributeName="transform" type="rotate"
      values="12 447 72; -8 447 72; 5 447 72; -3 447 72; 1.7 447 72; -1.7 447 72; 1.7 447 72"
      keyTimes="0; 0.12; 0.25; 0.38; 0.55; 0.78; 1"
      dur="7s" repeatCount="indefinite"/>

    <!-- Metal Swivel Clasp & Clip -->
    <g transform="translate(447, 68)">
      <!-- Oval Ring -->
      <ellipse cx="0" cy="0" rx="11" ry="8" fill="none" stroke="url(#{prefix}-metal-sheen)" stroke-width="3"/>
      <!-- Swivel Joint -->
      <rect x="-6" y="7" width="12" height="8" rx="2" fill="url(#{prefix}-metal-sheen)"/>
      <!-- Clasp Hook through badge slot -->
      <path d="M -4,15 L -4,34 Q 0,38 4,34 L 4,15 Z" fill="none" stroke="url(#{prefix}-metal-sheen)" stroke-width="3"/>
    </g>

    <!-- ================= THE ID BADGE CARD ================= -->
    <!-- Centered horizontally, width 570, height 365, from y=96 to 461 -->
    <g transform="translate(162, 96)">
      <!-- Badge Body -->
      <rect x="0" y="0" width="570" height="365" rx="22" fill="#0b1122"/>
      <rect x="0" y="0" width="570" height="365" rx="22" fill="url(#{prefix}-dots)"/>
      
      <!-- Top Slot Punch Hole for Clasp -->
      <rect x="260" y="10" width="50" height="10" rx="5" fill="#070b16" stroke="#334155" stroke-width="1.5"/>

      <!-- Header Ribbon -->
      <g transform="translate(24, 30)">
        <rect x="0" y="0" width="522" height="30" rx="6" fill="#141f36" stroke="#247bff" stroke-width="1" stroke-opacity="0.4"/>
        <circle cx="16" cy="15" r="4" fill="#247bff"/>
        <text x="28" y="20" class="{prefix}-mono" font-size="11" font-weight="600" fill="#f0f4fc" letter-spacing="1">DEFENSE INTELLIGENCE IDENTITY CREDENTIAL</text>
        <text x="460" y="20" class="{prefix}-mono" font-size="10.5" fill="#ff354f" font-weight="700">SEC-OP//04</text>
      </g>

      <!-- Left Column: Photo & Barcode -->
      <g transform="translate(24, 72)">
        <!-- Photo Frame -->
        <rect x="0" y="0" width="150" height="165" rx="16" fill="#070b16" stroke="url(#{prefix}-card-rim)" stroke-width="1.8"/>
        
        <!-- Base64 Photo Inlined -->
        <image href="data:image/png;base64,{id_b64}" x="-8" y="-4" width="166" height="166" clip-path="url(#{prefix}-photo-clip)" preserveAspectRatio="xMidYMid meet"/>
        
        <!-- Hologram Stamp on Photo Corner -->
        <g transform="translate(108, 126)">
          <circle cx="16" cy="16" r="16" fill="#070b16" fill-opacity="0.8" stroke="#247bff" stroke-width="1"/>
          <text x="16" y="20" class="{prefix}-mono" font-size="8" fill="#247bff" text-anchor="middle" font-weight="700">VERIFIED</text>
        </g>

        <!-- Barcode Graphic -->
        <g transform="translate(0, 180)">
          <rect x="0" y="0" width="150" height="46" rx="6" fill="#ffffff" fill-opacity="0.95"/>
          <!-- Barcode vertical lines -->
          <g stroke="#070b16" stroke-width="2">
            <line x1="8" y1="6" x2="8" y2="34"/>
            <line x1="12" y1="6" x2="12" y2="34" stroke-width="3"/>
            <line x1="18" y1="6" x2="18" y2="34" stroke-width="1"/>
            <line x1="22" y1="6" x2="22" y2="34" stroke-width="4"/>
            <line x1="30" y1="6" x2="30" y2="34" stroke-width="2"/>
            <line x1="36" y1="6" x2="36" y2="34" stroke-width="1"/>
            <line x1="42" y1="6" x2="42" y2="34" stroke-width="3"/>
            <line x1="48" y1="6" x2="48" y2="34" stroke-width="2"/>
            <line x1="54" y1="6" x2="54" y2="34" stroke-width="4"/>
            <line x1="62" y1="6" x2="62" y2="34" stroke-width="1"/>
            <line x1="68" y1="6" x2="68" y2="34" stroke-width="3"/>
            <line x1="74" y1="6" x2="74" y2="34" stroke-width="2"/>
            <line x1="82" y1="6" x2="82" y2="34" stroke-width="4"/>
            <line x1="90" y1="6" x2="90" y2="34" stroke-width="1"/>
            <line x1="96" y1="6" x2="96" y2="34" stroke-width="3"/>
            <line x1="104" y1="6" x2="104" y2="34" stroke-width="2"/>
            <line x1="110" y1="6" x2="110" y2="34" stroke-width="4"/>
            <line x1="118" y1="6" x2="118" y2="34" stroke-width="2"/>
            <line x1="124" y1="6" x2="124" y2="34" stroke-width="3"/>
            <line x1="130" y1="6" x2="130" y2="34" stroke-width="1"/>
            <line x1="136" y1="6" x2="136" y2="34" stroke-width="2"/>
            <line x1="142" y1="6" x2="142" y2="34" stroke-width="1"/>
          </g>
          <text x="75" y="42" font-family="monospace" font-size="7.5" fill="#070b16" text-anchor="middle" font-weight="700">* SG-2026-OCT-8724 *</text>
        </g>
      </g>

      <!-- Right Column: Verified Dated Metrics -->
      <g transform="translate(192, 74)">
        <!-- Name & Clearance -->
        <text x="0" y="24" class="{prefix}-sans" font-size="26" font-weight="700" fill="#f0f4fc">SAIL GAIKWAD</text>
        <text x="0" y="44" class="{prefix}-mono" font-size="12" font-weight="600" fill="#247bff" letter-spacing="0.5">RESEARCHER // AI DEFENSE &amp; DEV</text>

        <!-- Divider line -->
        <line x1="0" y1="56" x2="350" y2="56" stroke="#247bff" stroke-width="1" stroke-opacity="0.3"/>

        <!-- Metrics Grid -->
        <!-- Field 1 -->
        <g transform="translate(0, 72)">
          <text x="0" y="0" class="{prefix}-mono" font-size="10" fill="#64748b">GITHUB IDENTITY</text>
          <text x="0" y="17" class="{prefix}-mono" font-size="13" font-weight="600" fill="#cbd5e1">@sailgaikwad</text>
        </g>
        <g transform="translate(180, 72)">
          <text x="0" y="0" class="{prefix}-mono" font-size="10" fill="#64748b">PUBLIC REPOSITORIES</text>
          <text x="0" y="17" class="{prefix}-mono" font-size="13" font-weight="600" fill="#10b981">8+ Active Projects</text>
        </g>

        <!-- Field 2 -->
        <g transform="translate(0, 114)">
          <text x="0" y="0" class="{prefix}-mono" font-size="10" fill="#64748b">PRIMARY ARSENAL</text>
          <text x="0" y="17" class="{prefix}-mono" font-size="13" font-weight="600" fill="#cbd5e1">Python · Docker · Linux</text>
        </g>
        <g transform="translate(180, 114)">
          <text x="0" y="0" class="{prefix}-mono" font-size="10" fill="#64748b">VERIFIED TIMESTAMP</text>
          <text x="0" y="17" class="{prefix}-mono" font-size="13" font-weight="600" fill="#cbd5e1">OCTOBER 2026</text>
        </g>

        <!-- Field 3 -->
        <g transform="translate(0, 156)">
          <text x="0" y="0" class="{prefix}-mono" font-size="10" fill="#64748b">LOCATION HUB</text>
          <text x="0" y="17" class="{prefix}-mono" font-size="13" font-weight="600" fill="#cbd5e1">Maharashtra, IN</text>
        </g>
        <g transform="translate(180, 156)">
          <text x="0" y="0" class="{prefix}-mono" font-size="10" fill="#64748b">STATUS</text>
          <text x="0" y="17" class="{prefix}-mono" font-size="13" font-weight="600" fill="#247bff">COMMITTED TO MASTER</text>
        </g>

        <!-- Security Hash Fingerprint -->
        <g transform="translate(0, 198)">
          <rect x="0" y="0" width="354" height="26" rx="6" fill="#070b16" stroke="#247bff" stroke-width="1" stroke-opacity="0.3"/>
          <text x="12" y="17" class="{prefix}-mono" font-size="10" fill="#94a3b8">SHA256: 7b84a91f42e8d9e1c3b7a54820fed761</text>
        </g>
      </g>

      <!-- Foil / Light Sweep Overlay Layer -->
      <rect x="0" y="0" width="570" height="365" rx="22" fill="url(#{prefix}-foil-sweep)" pointer-events="none"/>

      <!-- Outer Hairline Gradient Border -->
      <rect x="1" y="1" width="568" height="363" rx="21" fill="none" stroke="url(#{prefix}-card-rim)" stroke-width="1.8"/>
    </g>
  </g>
</svg>"""
    return svg

# =========================================================================
# 5. assets/connect.svg
# =========================================================================
def build_connect():
    prefix = "conn"
    css = make_font_css(prefix)
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 895 380" width="100%" height="100%">
  <defs>
    <style>
      {css}
      .nudge-arrow {{ animation: {prefix}Nudge 1.8s ease-in-out infinite; }}
      @keyframes {prefix}Nudge {{ 0%, 100% {{ transform: translateX(0px); }} 50% {{ transform: translateX(8px); }} }}
    </style>
    
    <pattern id="{prefix}-dots" x="0" y="0" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.1" fill="#247bff" fill-opacity="0.14"/>
    </pattern>

    <linearGradient id="{prefix}-border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.75"/>
      <stop offset="50%" stop-color="#0e1b38" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.6"/>
    </linearGradient>

    <!-- Social Card Gradient Borders -->
    <linearGradient id="{prefix}-card-blue" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#247bff" stop-opacity="0.1"/>
    </linearGradient>
    <linearGradient id="{prefix}-card-crimson" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff354f" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.1"/>
    </linearGradient>
  </defs>

  <!-- Base Canvas -->
  <rect width="895" height="380" rx="18" fill="#070b16"/>
  <rect width="895" height="380" rx="18" fill="url(#{prefix}-dots)"/>
  <rect x="1" y="1" width="893" height="378" rx="17" fill="none" stroke="url(#{prefix}-border-grad)" stroke-width="1.5"/>

  <!-- Left Side: Pointing Character -->
  <g transform="translate(10, 15)">
    <!-- Base64 Character inlined, pointing RIGHT toward social cards -->
    <image href="data:image/png;base64,{pointing_b64}" x="0" y="0" width="350" height="350" preserveAspectRatio="xMidYMid meet"/>
  </g>

  <!-- Right Side: Generously Spaced Social Cards -->
  <g transform="translate(370, 32)">
    <!-- Header -->
    <g>
      <rect x="0" y="0" width="180" height="24" rx="6" fill="#0d1527" stroke="#247bff" stroke-width="1" stroke-opacity="0.4"/>
      <text x="10" y="16" class="{prefix}-mono" font-size="11" font-weight="600" fill="#247bff" letter-spacing="0.5">INITIATE CONNECTION</text>
    </g>
    <text x="0" y="54" class="{prefix}-sans" font-size="24" font-weight="700" fill="#f0f4fc">Let's Build Something Exceptional</text>
    <text x="0" y="74" class="{prefix}-sans" font-size="13" fill="#94a3b8">Open for security research, AI systems discussions, and engineering collaborations.</text>

    <!-- Social Cards Group -->
    <g transform="translate(0, 92)">
      <!-- Card 1: LinkedIn -->
      <g transform="translate(0, 0)">
        <rect x="0" y="0" width="480" height="52" rx="10" fill="#0b1122" stroke="url(#{prefix}-card-blue)" stroke-width="1.2"/>
        <!-- Platform Icon (LinkedIn) -->
        <rect x="12" y="10" width="32" height="32" rx="6" fill="#0a66c2"/>
        <text x="28" y="31" font-family="sans-serif" font-weight="700" font-size="17" fill="#ffffff" text-anchor="middle">in</text>
        <!-- Titles -->
        <text x="56" y="24" class="{prefix}-sans" font-size="14" font-weight="700" fill="#f0f4fc">LinkedIn</text>
        <text x="56" y="41" class="{prefix}-mono" font-size="11" fill="#94a3b8">linkedin.com/in/sailgaikwad</text>
        <!-- Nudging Arrow -->
        <g class="nudge-arrow">
          <text x="445" y="32" class="{prefix}-mono" font-size="18" fill="#247bff" font-weight="700">→</text>
        </g>
      </g>

      <!-- Card 2: GitHub -->
      <g transform="translate(0, 60)">
        <rect x="0" y="0" width="480" height="52" rx="10" fill="#0b1122" stroke="url(#{prefix}-card-crimson)" stroke-width="1.2"/>
        <!-- Platform Icon (GitHub) -->
        <rect x="12" y="10" width="32" height="32" rx="6" fill="#1f2937"/>
        <path d="M 28,14 C 22.5,14 18,18.5 18,24 C 18,28.4 20.9,32.2 24.8,33.5 C 25.3,33.6 25.5,33.3 25.5,33 C 25.5,32.8 25.5,32 25.5,31.2 C 22.7,31.8 22.1,29.9 22.1,29.9 C 21.7,28.7 21,28.4 21,28.4 C 20,27.8 21.1,27.8 21.1,27.8 C 22.2,27.9 22.8,29 22.8,29 C 23.8,30.6 25.3,30.2 25.9,29.9 C 26,29.2 26.3,28.7 26.6,28.4 C 24.4,28.1 22,27.3 22,23.5 C 22,22.4 22.4,21.5 23.1,20.8 C 23,20.5 22.6,19.5 23.2,18.1 C 23.2,18.1 24.1,17.8 26.1,19.2 C 27,18.9 27.9,18.8 28.9,18.8 C 29.8,18.8 30.8,18.9 31.7,19.2 C 33.7,17.8 34.6,18.1 34.6,18.1 C 35.2,19.5 34.8,20.5 34.7,20.8 C 35.4,21.5 35.8,22.4 35.8,23.5 C 35.8,27.3 33.4,28.1 31.2,28.4 C 31.6,28.7 32,29.4 32,30.4 C 32,31.9 32,33 32,33.4 C 32,33.7 32.2,34 32.7,33.9 C 36.7,32.5 39.5,28.7 39.5,24.2 C 39.5,18.5 35,14 28,14 Z" fill="#f0f4fc"/>
        <!-- Titles -->
        <text x="56" y="24" class="{prefix}-sans" font-size="14" font-weight="700" fill="#f0f4fc">GitHub</text>
        <text x="56" y="41" class="{prefix}-mono" font-size="11" fill="#94a3b8">github.com/sailgaikwad</text>
        <!-- Nudging Arrow -->
        <g class="nudge-arrow">
          <text x="445" y="32" class="{prefix}-mono" font-size="18" fill="#ff354f" font-weight="700">→</text>
        </g>
      </g>

      <!-- Card 3: Email -->
      <g transform="translate(0, 120)">
        <rect x="0" y="0" width="480" height="52" rx="10" fill="#0b1122" stroke="url(#{prefix}-card-blue)" stroke-width="1.2"/>
        <!-- Platform Icon (Email) -->
        <rect x="12" y="10" width="32" height="32" rx="6" fill="#ea4335"/>
        <path d="M 20,20 L 28,26 L 36,20 M 20,30 L 20,20 L 36,20 L 36,30 Z" fill="none" stroke="#ffffff" stroke-width="2" stroke-linejoin="round"/>
        <!-- Titles -->
        <text x="56" y="24" class="{prefix}-sans" font-size="14" font-weight="700" fill="#f0f4fc">Email Dispatch</text>
        <text x="56" y="41" class="{prefix}-mono" font-size="11" fill="#94a3b8">sailgaikwad108@gmail.com</text>
        <!-- Nudging Arrow -->
        <g class="nudge-arrow">
          <text x="445" y="32" class="{prefix}-mono" font-size="18" fill="#247bff" font-weight="700">→</text>
        </g>
      </g>

      <!-- Card 4: Facebook -->
      <g transform="translate(0, 180)">
        <rect x="0" y="0" width="480" height="52" rx="10" fill="#0b1122" stroke="url(#{prefix}-card-crimson)" stroke-width="1.2"/>
        <!-- Platform Icon (Facebook) -->
        <rect x="12" y="10" width="32" height="32" rx="6" fill="#1877f2"/>
        <text x="28" y="32" font-family="sans-serif" font-weight="700" font-size="20" fill="#ffffff" text-anchor="middle">f</text>
        <!-- Titles -->
        <text x="56" y="24" class="{prefix}-sans" font-size="14" font-weight="700" fill="#f0f4fc">Facebook Profile</text>
        <text x="56" y="41" class="{prefix}-mono" font-size="11" fill="#94a3b8">facebook.com/sailgaikwad</text>
        <!-- Nudging Arrow -->
        <g class="nudge-arrow">
          <text x="445" y="32" class="{prefix}-mono" font-size="18" fill="#ff354f" font-weight="700">→</text>
        </g>
      </g>
    </g>
  </g>
</svg>"""
    return svg

# =========================================================================
# 6. README.md
# =========================================================================
def build_readme():
    return """<div align="center">

<!-- ================= 01 HERO SECTION ================= -->
![Intro](./assets/hero.svg?v=1)

<!-- ================= 02 CAPABILITIES & PASSIONS CAROUSEL ================= -->
![About](./assets/about-life.svg?v=1)

<!-- ================= 03 TECH RADAR & ORBITS ================= -->
![Stack](./assets/stack.svg?v=1)

<!-- ================= 04 PENDULUM ID DASHBOARD ================= -->
![ID](./assets/id-dashboard.svg?v=1)

<!-- ================= 05 CONNECT WITH POINTING CHARACTER ================= -->
![Connect](./assets/connect.svg?v=1)

<br>

<!-- ================= 06 VERIFIED PROFILE IDENTITY ================= -->
<p align="center">
  <a href="https://linkedin.com/in/sailgaikwad" target="_blank">
    <img src="./assets/sail.png" alt="Sail Gaikwad — Security Researcher & Systems Architect" width="240" />
  </a>
</p>
<p align="center">
  <strong>Sail Gaikwad</strong><br>
  <sub>Cybersecurity Researcher · AI Safety &amp; LLM Defense · Autonomous Systems Builder</sub>
</p>

<br>

<!-- ================= CLICKABLE SOCIAL DISPATCH BUTTONS ================= -->
<p align="center">
  <a href="https://linkedin.com/in/sailgaikwad" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  &nbsp;&nbsp;
  <a href="https://github.com/sailgaikwad" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-070B16?style=for-the-badge&logo=github&logoColor=247BFF" alt="GitHub" />
  </a>
  &nbsp;&nbsp;
  <a href="mailto:sailgaikwad108@gmail.com" target="_blank">
    <img src="https://img.shields.io/badge/Email-FF354F?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
  </a>
  &nbsp;&nbsp;
  <a href="https://facebook.com/sailgaikwad" target="_blank">
    <img src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook" />
  </a>
</p>

</div>

---

### 🛡️ Featured Work & Research Repositories

| Repository | Domain / Focus | Key Technologies | Status |
| :--- | :--- | :--- | :--- |
| [**ai-supply-chain-security**](https://github.com/sailgaikwad/ai-supply-chain-security) | AI Model & Dependency Integrity, Vulnerability Scanning | Python, ML Security, Docker | ⚡ Active |
| [**FitnessTracker**](https://github.com/sailgaikwad/FitnessTracker) | Health Metrics, Automated Tracking & Analytics Engine | Python, Data Processing, SQLite | ⚡ Active |
| [**NoteVault**](https://github.com/sailgaikwad/NoteVault) | Encrypted Note Storage, Client-Side Security & State | JavaScript, Web Crypto, Node.js | ⚡ Active |
| [**Mayur-Driving-School**](https://github.com/sailgaikwad/Mayur-Driving-School) | Mobile Scheduling & Management Application | Kotlin, Android SDK, Gradle | ⚡ Active |

---

<div align="center">
  <sub>Built with the <strong>Profile Playbook</strong> · Deep Navy <code>#070B16</code> · Electric Blue <code>#247BFF</code> · Crimson <code>#FF354F</code></sub>
</div>
"""

# =========================================================================
# 7. preview.html
# =========================================================================
def build_preview_html():
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GitHub Profile Playbook Live Preview — Sail Gaikwad</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: #030712;
      color: #f1f5f9;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      padding: 40px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .header-bar {
      max-width: 920px;
      width: 100%;
      margin-bottom: 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 16px;
      border-bottom: 1px solid #1e293b;
    }
    .badge {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 9999px;
      font-size: 12px;
      font-weight: 600;
      background: #141f36;
      color: #247bff;
      border: 1px solid rgba(36, 123, 255, 0.4);
    }
    .container {
      max-width: 895px;
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    .svg-wrapper {
      width: 100%;
      border-radius: 18px;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .svg-wrapper img {
      width: 100%;
      height: auto;
      display: block;
    }
    .links-bar {
      margin-top: 16px;
      display: flex;
      justify-content: center;
      gap: 16px;
    }
    .links-bar a {
      display: inline-block;
      transition: transform 0.2s;
    }
    .links-bar a:hover {
      transform: translateY(-2px);
    }
  </style>
</head>
<body>
  <div class="header-bar">
    <div>
      <h1 style="font-size: 20px; font-weight: 700;">GitHub Profile Playbook Preview</h1>
      <p style="font-size: 13px; color: #94a3b8; margin-top: 4px;">Verified Self-Contained SVG Suite with SMIL Motion &amp; Base64 Assets</p>
    </div>
    <span class="badge">100% GITHUB SAFE</span>
  </div>

  <div class="container">
    <!-- 01 Hero -->
    <div class="svg-wrapper">
      <img src="./assets/hero.svg?v=1" alt="Hero">
    </div>

    <!-- 02 About Life Carousel -->
    <div class="svg-wrapper">
      <img src="./assets/about-life.svg?v=1" alt="About Life">
    </div>

    <!-- 03 Stack Orbits -->
    <div class="svg-wrapper">
      <img src="./assets/stack.svg?v=1" alt="Tech Stack">
    </div>

    <!-- 04 ID Dashboard Pendulum -->
    <div class="svg-wrapper">
      <img src="./assets/id-dashboard.svg?v=1" alt="ID Dashboard">
    </div>

    <!-- 05 Connect -->
    <div class="svg-wrapper">
      <img src="./assets/connect.svg?v=1" alt="Connect">
    </div>

    <!-- 06 Verified Profile Identity -->
    <div style="display: flex; flex-direction: column; align-items: center; margin: 12px 0 6px;">
      <a href="https://linkedin.com/in/sailgaikwad" target="_blank">
        <img src="./assets/sail.png" alt="Sail Gaikwad" style="width: 240px; height: auto; border-radius: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.6);" />
      </a>
      <p style="margin-top: 12px; font-size: 15px; font-weight: 600; color: #f0f4fc;">Sail Gaikwad</p>
      <p style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Cybersecurity Researcher · AI Safety &amp; LLM Defense · Autonomous Systems</p>
    </div>

    <!-- Clickable Social Links -->
    <div class="links-bar">
      <a href="https://linkedin.com/in/sailgaikwad" target="_blank">
        <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
      </a>
      <a href="https://github.com/sailgaikwad" target="_blank">
        <img src="https://img.shields.io/badge/GitHub-070B16?style=for-the-badge&logo=github&logoColor=247BFF" alt="GitHub">
      </a>
      <a href="mailto:sailgaikwad108@gmail.com" target="_blank">
        <img src="https://img.shields.io/badge/Email-FF354F?style=for-the-badge&logo=gmail&logoColor=white" alt="Email">
      </a>
      <a href="https://facebook.com/sailgaikwad" target="_blank">
        <img src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook">
      </a>
    </div>
  </div>
</body>
</html>
"""

def main():
    print("Writing assets/hero.svg...")
    with open(os.path.join(ASSETS_DIR, "hero.svg"), "w", encoding="utf-8") as f:
        f.write(build_hero())

    print("Writing assets/about-life.svg...")
    with open(os.path.join(ASSETS_DIR, "about-life.svg"), "w", encoding="utf-8") as f:
        f.write(build_about_life())

    print("Writing assets/stack.svg...")
    with open(os.path.join(ASSETS_DIR, "stack.svg"), "w", encoding="utf-8") as f:
        f.write(build_stack())

    print("Writing assets/id-dashboard.svg...")
    with open(os.path.join(ASSETS_DIR, "id-dashboard.svg"), "w", encoding="utf-8") as f:
        f.write(build_id_dashboard())

    print("Writing assets/connect.svg...")
    with open(os.path.join(ASSETS_DIR, "connect.svg"), "w", encoding="utf-8") as f:
        f.write(build_connect())

    print("Writing README.md...")
    with open(os.path.join(WORKSPACE_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write(build_readme())

    print("Writing preview.html...")
    with open(os.path.join(WORKSPACE_DIR, "preview.html"), "w", encoding="utf-8") as f:
        f.write(build_preview_html())

    # Build upload-ready ZIP
    zip_path = os.path.join(WORKSPACE_DIR, "profile-playbook-package.zip")
    print(f"Creating upload-ready ZIP: {zip_path}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(os.path.join(WORKSPACE_DIR, "README.md"), arcname="README.md")
        for fname in ["hero.svg", "about-life.svg", "stack.svg", "id-dashboard.svg", "connect.svg", "id.png", "right_pointing.png", "sail.png"]:
            p = os.path.join(ASSETS_DIR, fname)
            if os.path.exists(p):
                zipf.write(p, arcname=f"assets/{fname}")
    print("ZIP package generated successfully!")

if __name__ == "__main__":
    main()
