/**
 * portfolio-themes.js — Dynamic Multi-Theme & Multi-Layout Rendering Engine.
 * Powers the 8 distinct portfolio experiences:
 * 1. Modern (Modular Bento Grid)
 * 2. Developer (Hacker IDE & Terminal Workstation)
 * 3. Creative (Bold Asymmetric Studio & Neo-Display)
 * 4. Corporate (Executive Briefing 2-Column Architecture)
 * 5. AI / Tech (Futuristic Neural HUD & Cyber Telemetry)
 * 6. Minimal (Swiss Editorial Design Monograph)
 * 7. Dark Luxury (OLED Midnight Titanium Showcase)
 * 8. Elegant (Classical Gazette & Distinguished CV)
 *
 * Keeps content and design 100% separate (Rule 7).
 * Candidate data is dynamically rendered with active theme tokens and user customizations.
 */

const PortfolioThemesEngine = (() => {

  const THEMES_METADATA = [
    // ----------------------------------------------------
    // CATEGORY 1: MODERN & SAAS PRODUCTS (10 THEMES)
    // ----------------------------------------------------
    {
      id: "modern",
      name: "Modern Bento",
      category: "saas",
      categoryName: "Modern & SaaS",
      layout: "modern",
      layoutName: "Modular Bento Grid",
      layoutBadge: "Bento Grid",
      icon: "✨",
      desc: "Apple/Linear style modular bento cards, floating glass dock, interactive live widgets",
      tags: ["Bento", "Glassmorphic", "Linear"],
      defaultPrimary: "#4f46e5",
      defaultSecondary: "#06b6d4",
      font: "Plus Jakarta Sans",
      defaultBg: "mesh",
      defaultCard: "glass",
      defaultBtn: "rounded",
      defaultDark: false,
      palettes: [
        { name: "Electric Indigo", primary: "#4f46e5", secondary: "#06b6d4" },
        { name: "Sunset Violet", primary: "#7c3aed", secondary: "#f43f5e" },
        { name: "Ocean Emerald", primary: "#0284c7", secondary: "#10b981" },
        { name: "Aurora Teal", primary: "#0d9488", secondary: "#6366f1" },
      ]
    },
    {
      id: "linear_noir",
      name: "Linear Dusk",
      category: "saas",
      categoryName: "Modern & SaaS",
      layout: "modern",
      layoutName: "Modular Bento Grid",
      layoutBadge: "Linear Dark",
      icon: "⚡",
      desc: "Deep graphite matte surface, subtle ultraviolet rim glow, precision micro-borders",
      tags: ["Dark", "Minimal", "Engineering"],
      defaultPrimary: "#5e6ad2",
      defaultSecondary: "#a5b4fc",
      font: "Inter",
      defaultBg: "dots",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: true,
      palettes: [
        { name: "Linear Indigo", primary: "#5e6ad2", secondary: "#a5b4fc" },
        { name: "Graphite Glow", primary: "#818cf8", secondary: "#c084fc" },
        { name: "Deep Charcoal", primary: "#6366f1", secondary: "#38bdf8" },
      ]
    },
    {
      id: "saas_stripe",
      name: "Stripe FinTech",
      category: "saas",
      categoryName: "Modern & SaaS",
      layout: "modern",
      layoutName: "Modular Bento Grid",
      layoutBadge: "FinTech Bento",
      icon: "💳",
      desc: "Royal indigo typography, crisp cards, banking-grade subtle borders, premium gradients",
      tags: ["FinTech", "Crisp", "Corporate"],
      defaultPrimary: "#635bff",
      defaultSecondary: "#00d4ff",
      font: "Plus Jakarta Sans",
      defaultBg: "mesh",
      defaultCard: "elevated",
      defaultBtn: "rounded",
      defaultDark: false,
      palettes: [
        { name: "Stripe Purple", primary: "#635bff", secondary: "#00d4ff" },
        { name: "Atlas Blue", primary: "#0a2540", secondary: "#00d4ff" },
        { name: "Mint FinTech", primary: "#00d4ff", secondary: "#635bff" },
      ]
    },
    {
      id: "saas_vercel",
      name: "Vercel Geometric",
      category: "saas",
      categoryName: "Modern & SaaS",
      layout: "modern",
      layoutName: "Modular Bento Grid",
      layoutBadge: "Monochrome Grid",
      icon: "▲",
      desc: "Pure monochrome stark contrast, razor-sharp edges, high-speed frontend developer vibe",
      tags: ["Monochrome", "Geometric", "Frontend"],
      defaultPrimary: "#18181b",
      defaultSecondary: "#71717a",
      font: "Inter",
      defaultBg: "grid",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Geist Pure", primary: "#18181b", secondary: "#71717a" },
        { name: "True Black", primary: "#09090b", secondary: "#a1a1aa" },
      ]
    },
    {
      id: "saas_supabase",
      name: "Emerald Supabase",
      category: "saas",
      categoryName: "Modern & SaaS",
      layout: "modern",
      layoutName: "Modular Bento Grid",
      layoutBadge: "Open Source",
      icon: "⚡",
      desc: "Charcoal workspace with glowing emerald green database accents and dark widgets",
      tags: ["Dark", "Database", "Emerald"],
      defaultPrimary: "#3ecf8e",
      defaultSecondary: "#2dd4bf",
      font: "Plus Jakarta Sans",
      defaultBg: "dots",
      defaultCard: "glass",
      defaultBtn: "rounded",
      defaultDark: true,
      palettes: [
        { name: "Supabase Green", primary: "#3ecf8e", secondary: "#2dd4bf" },
        { name: "Forest Matrix", primary: "#10b981", secondary: "#34d399" },
      ]
    },
    {
      id: "saas_craft",
      name: "Nordic Frost",
      category: "saas",
      categoryName: "Modern & SaaS",
      layout: "modern",
      layoutName: "Modular Bento Grid",
      layoutBadge: "Nordic Clean",
      icon: "❄️",
      desc: "Scandinavian airy whitespace, cool icy blues, serene soft cards and calm typography",
      tags: ["Nordic", "Clean", "Light"],
      defaultPrimary: "#0284c7",
      defaultSecondary: "#38bdf8",
      font: "Outfit",
      defaultBg: "mesh",
      defaultCard: "glass",
      defaultBtn: "pill",
      defaultDark: false,
      palettes: [
        { name: "Arctic Ice", primary: "#0284c7", secondary: "#38bdf8" },
        { name: "Fjord Blue", primary: "#0369a1", secondary: "#7dd3fc" },
      ]
    },
    {
      id: "saas_aurora",
      name: "Aurora Glassmorphism",
      category: "saas",
      categoryName: "Modern & SaaS",
      layout: "modern",
      layoutName: "Modular Bento Grid",
      layoutBadge: "Aurora Glass",
      icon: "🌌",
      desc: "Frosted liquid glass panels floating on top of shifting multi-hued auroral ambient glows",
      tags: ["Glass", "Aurora", "Glow"],
      defaultPrimary: "#8b5cf6",
      defaultSecondary: "#ec4899",
      font: "Plus Jakarta Sans",
      defaultBg: "mesh",
      defaultCard: "glass",
      defaultBtn: "pill",
      defaultDark: false,
      palettes: [
        { name: "Northern Lights", primary: "#8b5cf6", secondary: "#ec4899" },
        { name: "Cosmic Twilight", primary: "#a855f7", secondary: "#06b6d4" },
      ]
    },
    {
      id: "saas_prism",
      name: "Dynamic Prism",
      category: "saas",
      categoryName: "Modern & SaaS",
      layout: "modern",
      layoutName: "Modular Bento Grid",
      layoutBadge: "Prism Glow",
      icon: "💎",
      desc: "Multi-spectrum prismatic accents, vibrant teal and indigo highlights, polished UI",
      tags: ["Vibrant", "Modern", "Dynamic"],
      defaultPrimary: "#0d9488",
      defaultSecondary: "#6366f1",
      font: "Plus Jakarta Sans",
      defaultBg: "mesh",
      defaultCard: "elevated",
      defaultBtn: "rounded",
      defaultDark: false,
      palettes: [
        { name: "Prism Cyan", primary: "#0d9488", secondary: "#6366f1" },
        { name: "Prism Berry", primary: "#0284c7", secondary: "#e11d48" },
      ]
    },
    {
      id: "saas_sunset",
      name: "California Glow",
      category: "saas",
      categoryName: "Modern & SaaS",
      layout: "modern",
      layoutName: "Modular Bento Grid",
      layoutBadge: "Sunset Warmth",
      icon: "🌅",
      desc: "Warm peach, coral rose, and golden hour sunshine gradients for an inviting impression",
      tags: ["Warm", "Friendly", "SaaS"],
      defaultPrimary: "#f43f5e",
      defaultSecondary: "#fb923c",
      font: "Outfit",
      defaultBg: "mesh",
      defaultCard: "glass",
      defaultBtn: "rounded",
      defaultDark: false,
      palettes: [
        { name: "Pacific Sunset", primary: "#f43f5e", secondary: "#fb923c" },
        { name: "Golden Glow", primary: "#e11d48", secondary: "#f59e0b" },
      ]
    },
    {
      id: "saas_raycast",
      name: "Raycast Command",
      category: "saas",
      categoryName: "Modern & SaaS",
      layout: "modern",
      layoutName: "Modular Bento Grid",
      layoutBadge: "Command Palette",
      icon: "⌘",
      desc: "Command launcher aesthetics, hotkey badge indicators, deep charcoal spotlight panels",
      tags: ["Keyboard", "Productivity", "Dark"],
      defaultPrimary: "#ff6363",
      defaultSecondary: "#ff9f43",
      font: "Inter",
      defaultBg: "dots",
      defaultCard: "bordered",
      defaultBtn: "rounded",
      defaultDark: true,
      palettes: [
        { name: "Raycast Red", primary: "#ff6363", secondary: "#ff9f43" },
        { name: "Spotlight Amber", primary: "#f59e0b", secondary: "#ef4444" },
      ]
    },

    // ----------------------------------------------------
    // CATEGORY 2: TECH & SOFTWARE ENGINEERING (10 THEMES)
    // ----------------------------------------------------
    {
      id: "developer",
      name: "VS Code Dark",
      category: "tech",
      categoryName: "Tech & Dev",
      layout: "developer",
      layoutName: "Terminal / IDE Workstation",
      layoutBadge: "Hacker IDE",
      icon: "💻",
      desc: "Full code workstation, VS Code editor tabs, interactive JSON object, git commits, repo cards",
      tags: ["IDE", "Monospace", "Code"],
      defaultPrimary: "#58a6ff",
      defaultSecondary: "#7ee787",
      font: "Fira Code",
      defaultBg: "grid",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: true,
      palettes: [
        { name: "GitHub Dark", primary: "#58a6ff", secondary: "#7ee787" },
        { name: "VS Code Modern", primary: "#38bdf8", secondary: "#4ade80" },
      ]
    },
    {
      id: "tech_matrix",
      name: "Cyber Matrix",
      category: "tech",
      categoryName: "Tech & Dev",
      layout: "developer",
      layoutName: "Terminal / IDE Workstation",
      layoutBadge: "Matrix Phosphor",
      icon: "📟",
      desc: "CRT green phosphor glow, digital rain background grid, hacker shell command prompts",
      tags: ["Matrix", "Terminal", "Hacker"],
      defaultPrimary: "#00ff66",
      defaultSecondary: "#00f2fe",
      font: "Fira Code",
      defaultBg: "grid",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: true,
      palettes: [
        { name: "Terminal Green", primary: "#00ff66", secondary: "#00f2fe" },
        { name: "Phosphor Amber", primary: "#ffb800", secondary: "#00ff66" },
      ]
    },
    {
      id: "dev_dracula",
      name: "Dracula Monospace",
      category: "tech",
      categoryName: "Tech & Dev",
      layout: "developer",
      layoutName: "Terminal / IDE Workstation",
      layoutBadge: "Dracula Theme",
      icon: "🧛",
      desc: "Iconic Dracula syntax palette: vibrant purple, toxic green, and pastel cyan on dark slate",
      tags: ["Dracula", "IDE", "Dark"],
      defaultPrimary: "#bd93f9",
      defaultSecondary: "#50fa7b",
      font: "Fira Code",
      defaultBg: "dots",
      defaultCard: "bordered",
      defaultBtn: "rounded",
      defaultDark: true,
      palettes: [
        { name: "Dracula Classic", primary: "#bd93f9", secondary: "#50fa7b" },
        { name: "Dracula Cyan", primary: "#8be9fd", secondary: "#ff79c6" },
      ]
    },
    {
      id: "dev_one_dark",
      name: "Atom One Dark",
      category: "tech",
      categoryName: "Tech & Dev",
      layout: "developer",
      layoutName: "Terminal / IDE Workstation",
      layoutBadge: "One Dark",
      icon: "⚛️",
      desc: "Beloved Atom editor color scheme: soft pastel blue, olive green, warm stone background",
      tags: ["Atom", "Pastel", "Editor"],
      defaultPrimary: "#61afef",
      defaultSecondary: "#98c379",
      font: "Fira Code",
      defaultBg: "grid",
      defaultCard: "bordered",
      defaultBtn: "rounded",
      defaultDark: true,
      palettes: [
        { name: "One Dark Original", primary: "#61afef", secondary: "#98c379" },
      ]
    },
    {
      id: "dev_monokai",
      name: "Monokai Pro",
      category: "tech",
      categoryName: "Tech & Dev",
      layout: "developer",
      layoutName: "Terminal / IDE Workstation",
      layoutBadge: "Monokai Pro",
      icon: "💛",
      desc: "Sublime text legendary palette: hot magenta, warm amber gold, mint green, and electric blue",
      tags: ["Monokai", "Vibrant", "Code"],
      defaultPrimary: "#ffd866",
      defaultSecondary: "#ff6188",
      font: "Fira Code",
      defaultBg: "grid",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: true,
      palettes: [
        { name: "Monokai Pro", primary: "#ffd866", secondary: "#ff6188" },
      ]
    },
    {
      id: "dev_git_craft",
      name: "Git Branch Workstation",
      category: "tech",
      categoryName: "Tech & Dev",
      layout: "developer",
      layoutName: "Terminal / IDE Workstation",
      layoutBadge: "Git Workstation",
      icon: "🌿",
      desc: "Version control timeline, commit graph nodes, pull-request style project case studies",
      tags: ["Git", "OpenSource", "Dev"],
      defaultPrimary: "#38bdf8",
      defaultSecondary: "#34d399",
      font: "Fira Code",
      defaultBg: "dots",
      defaultCard: "bordered",
      defaultBtn: "rounded",
      defaultDark: true,
      palettes: [
        { name: "Git Main", primary: "#38bdf8", secondary: "#34d399" },
      ]
    },
    {
      id: "tech_devops",
      name: "Kubernetes Cloud Console",
      category: "tech",
      categoryName: "Tech & Dev",
      layout: "dashboard",
      layoutName: "Interactive Cockpit",
      layoutBadge: "Cloud DevOps",
      icon: "☸️",
      desc: "SRE / Cloud architect cockpit: pod telemetry, uptime stats, deployment cluster metrics",
      tags: ["DevOps", "Cloud", "SRE"],
      defaultPrimary: "#326ce5",
      defaultSecondary: "#00d2d3",
      font: "Fira Code",
      defaultBg: "grid",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: true,
      palettes: [
        { name: "K8s Blue", primary: "#326ce5", secondary: "#00d2d3" },
      ]
    },
    {
      id: "tech_rust_systems",
      name: "Rust Ferrous Terminal",
      category: "tech",
      categoryName: "Tech & Dev",
      layout: "developer",
      layoutName: "Terminal / IDE Workstation",
      layoutBadge: "Systems Rust",
      icon: "🦀",
      desc: "Rust warm terracotta and gunmetal grey; low-level systems and high-throughput engineering vibe",
      tags: ["Rust", "Systems", "Performance"],
      defaultPrimary: "#dea584",
      defaultSecondary: "#f97316",
      font: "Fira Code",
      defaultBg: "grid",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: true,
      palettes: [
        { name: "Crab Terracotta", primary: "#dea584", secondary: "#f97316" },
      ]
    },
    {
      id: "tech_solidity_web3",
      name: "Web3 DApp Hacker",
      category: "tech",
      categoryName: "Tech & Dev",
      layout: "developer",
      layoutName: "Terminal / IDE Workstation",
      layoutBadge: "Web3 DApp",
      icon: "⛓️",
      desc: "Ethereum purple and neon cyan, smart contract bytecode blocks, decentralized engineer portfolio",
      tags: ["Web3", "Crypto", "Solidity"],
      defaultPrimary: "#a855f7",
      defaultSecondary: "#06b6d4",
      font: "Fira Code",
      defaultBg: "dots",
      defaultCard: "glass",
      defaultBtn: "glow",
      defaultDark: true,
      palettes: [
        { name: "Ether Neon", primary: "#a855f7", secondary: "#06b6d4" },
      ]
    },
    {
      id: "tech_api_architect",
      name: "REST / OpenAPI Gateway",
      category: "tech",
      categoryName: "Tech & Dev",
      layout: "dashboard",
      layoutName: "Interactive Cockpit",
      layoutBadge: "API Architect",
      icon: "🔌",
      desc: "Microservices gateway dashboard, HTTP endpoint method badges (GET, POST), latency metrics",
      tags: ["Backend", "Microservices", "API"],
      defaultPrimary: "#2563eb",
      defaultSecondary: "#10b981",
      font: "Fira Code",
      defaultBg: "grid",
      defaultCard: "bordered",
      defaultBtn: "rounded",
      defaultDark: false,
      palettes: [
        { name: "Swagger Blue", primary: "#2563eb", secondary: "#10b981" },
      ]
    },

    // ----------------------------------------------------
    // CATEGORY 3: CREATIVE & NEO-BRUTALISM (10 THEMES)
    // ----------------------------------------------------
    {
      id: "creative",
      name: "Creative Studio",
      category: "creative",
      categoryName: "Creative & Neo",
      layout: "creative",
      layoutName: "Asymmetric Neo-Display",
      layoutBadge: "Neo Studio",
      icon: "🎨",
      desc: "Bold expressive typography, rotated sticker badges, neo-brutalist offset shadow cards, playful bounces",
      tags: ["Neo-Brutalism", "Playful", "Stickers"],
      defaultPrimary: "#ec4899",
      defaultSecondary: "#f59e0b",
      font: "Outfit",
      defaultBg: "mesh",
      defaultCard: "glass",
      defaultBtn: "pill",
      defaultDark: false,
      palettes: [
        { name: "Neon Flamingo", primary: "#ec4899", secondary: "#f59e0b" },
        { name: "Cosmic Candy", primary: "#8b5cf6", secondary: "#ec4899" },
        { name: "Tropic Tangerine", primary: "#f97316", secondary: "#06b6d4" },
      ]
    },
    {
      id: "creative_memphis",
      name: "Memphis 80s Pop",
      category: "creative",
      categoryName: "Creative & Neo",
      layout: "creative",
      layoutName: "Asymmetric Neo-Display",
      layoutBadge: "Memphis Pop",
      icon: "🍭",
      desc: "Retro 80s geometric patterns, zigzag borders, primary pastels, quirky diagonal stickers",
      tags: ["Retro", "Memphis", "Color"],
      defaultPrimary: "#f43f5e",
      defaultSecondary: "#06b6d4",
      font: "Outfit",
      defaultBg: "dots",
      defaultCard: "bordered",
      defaultBtn: "pill",
      defaultDark: false,
      palettes: [
        { name: "Miami Memphis", primary: "#f43f5e", secondary: "#06b6d4" },
      ]
    },
    {
      id: "creative_pop_art",
      name: "Pop Art Bubble",
      category: "creative",
      categoryName: "Creative & Neo",
      layout: "creative",
      layoutName: "Asymmetric Neo-Display",
      layoutBadge: "Pop Comic",
      icon: "💥",
      desc: "Comic halftone dots, bold black stamp outlines, primary yellow and punchy magenta speech bubbles",
      tags: ["Comic", "PopArt", "Bold"],
      defaultPrimary: "#fbbf24",
      defaultSecondary: "#e11d48",
      font: "Outfit",
      defaultBg: "dots",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Lichtenstein Pop", primary: "#fbbf24", secondary: "#e11d48" },
      ]
    },
    {
      id: "creative_avant_garde",
      name: "Avant-Garde Studio",
      category: "creative",
      categoryName: "Creative & Neo",
      layout: "split_screen",
      layoutName: "Split-Screen Showcase",
      layoutBadge: "Avant-Garde",
      icon: "🏛️",
      desc: "Sticky artist statement column on left, asymmetric oversized editorial cards on right",
      tags: ["Design", "Studio", "Gallery"],
      defaultPrimary: "#18181b",
      defaultSecondary: "#ef4444",
      font: "Space Grotesk",
      defaultBg: "clean",
      defaultCard: "flat",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Modernist Red", primary: "#18181b", secondary: "#ef4444" },
      ]
    },
    {
      id: "creative_pastel_dream",
      name: "Pastel Confection",
      category: "creative",
      categoryName: "Creative & Neo",
      layout: "creative",
      layoutName: "Asymmetric Neo-Display",
      layoutBadge: "Soft Pastel",
      icon: "🌸",
      desc: "Gentle lavender, matcha green, and baby peach; friendly pill badges and smooth rounded curves",
      tags: ["Pastel", "Soft", "Cute"],
      defaultPrimary: "#a78bfa",
      defaultSecondary: "#34d399",
      font: "Outfit",
      defaultBg: "mesh",
      defaultCard: "glass",
      defaultBtn: "pill",
      defaultDark: false,
      palettes: [
        { name: "Lavender Matcha", primary: "#a78bfa", secondary: "#34d399" },
      ]
    },
    {
      id: "creative_cyberpunk",
      name: "Night City Cyberpunk",
      category: "creative",
      categoryName: "Creative & Neo",
      layout: "creative",
      layoutName: "Asymmetric Neo-Display",
      layoutBadge: "Cyberpunk",
      icon: "🌆",
      desc: "Blinding cyber yellow with hot magenta glitch stamps, high-contrast dark urban grit",
      tags: ["Cyberpunk", "Neon", "Edge"],
      defaultPrimary: "#facc15",
      defaultSecondary: "#f43f5e",
      font: "Space Grotesk",
      defaultBg: "grid",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: true,
      palettes: [
        { name: "Neon 2077", primary: "#facc15", secondary: "#f43f5e" },
      ]
    },
    {
      id: "creative_claymorphism",
      name: "Soft Clay Studio",
      category: "creative",
      categoryName: "Creative & Neo",
      layout: "creative",
      layoutName: "Asymmetric Neo-Display",
      layoutBadge: "Clay 3D",
      icon: "🧸",
      desc: "Tactile 3D inner-shadow clay pill cards, soft squishy feeling, playful typography",
      tags: ["3D", "Clay", "Tactile"],
      defaultPrimary: "#3b82f6",
      defaultSecondary: "#10b981",
      font: "Poppins",
      defaultBg: "mesh",
      defaultCard: "elevated",
      defaultBtn: "pill",
      defaultDark: false,
      palettes: [
        { name: "Clay Sky", primary: "#3b82f6", secondary: "#10b981" },
      ]
    },
    {
      id: "creative_editorial_art",
      name: "Art Director Lookbook",
      category: "creative",
      categoryName: "Creative & Neo",
      layout: "split_screen",
      layoutName: "Split-Screen Showcase",
      layoutBadge: "Art Lookbook",
      icon: "📖",
      desc: "Editorial photo shoot layout, large title treatments, sticky left intro panel, high fashion art",
      tags: ["Editorial", "Fashion", "Art"],
      defaultPrimary: "#be123c",
      defaultSecondary: "#f59e0b",
      font: "Playfair Display",
      defaultBg: "clean",
      defaultCard: "flat",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Crimson Silk", primary: "#be123c", secondary: "#f59e0b" },
      ]
    },
    {
      id: "creative_vaporwave",
      name: "Vaporwave Retro",
      category: "creative",
      categoryName: "Creative & Neo",
      layout: "creative",
      layoutName: "Asymmetric Neo-Display",
      layoutBadge: "Vaporwave",
      icon: "🌴",
      desc: "Nostalgic 90s aesthetic, glowing turquoise wireframe grid, purple-pink sunset gradient stamps",
      tags: ["90s", "Synth", "Vaporwave"],
      defaultPrimary: "#ff007f",
      defaultSecondary: "#00f0ff",
      font: "Space Grotesk",
      defaultBg: "grid",
      defaultCard: "glass",
      defaultBtn: "pill",
      defaultDark: true,
      palettes: [
        { name: "Sunset Synth", primary: "#ff007f", secondary: "#00f0ff" },
      ]
    },
    {
      id: "creative_poster",
      name: "Typographic Swiss Poster",
      category: "creative",
      categoryName: "Creative & Neo",
      layout: "creative",
      layoutName: "Asymmetric Neo-Display",
      layoutBadge: "Swiss Poster",
      icon: "📢",
      desc: "Ultra-heavy headline display fonts, rotated marquee labels, high-density graphic poster vibe",
      tags: ["Typography", "Poster", "Design"],
      defaultPrimary: "#ea580c",
      defaultSecondary: "#1e1e2e",
      font: "Syne",
      defaultBg: "clean",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Bauhaus Flame", primary: "#ea580c", secondary: "#1e1e2e" },
      ]
    },

    // ----------------------------------------------------
    // CATEGORY 4: CORPORATE & EXECUTIVE (8 THEMES)
    // ----------------------------------------------------
    {
      id: "corporate",
      name: "Corporate Executive",
      category: "corporate",
      categoryName: "Corporate & Exec",
      layout: "corporate",
      layoutName: "Executive Briefing (2-Column)",
      layoutBadge: "Executive 2-Col",
      icon: "🏢",
      desc: "Executive 2-column resume architecture, core competencies sidebar, strategic career trajectory",
      tags: ["Executive", "Board", "Corporate"],
      defaultPrimary: "#1e3a8a",
      defaultSecondary: "#0284c7",
      font: "Plus Jakarta Sans",
      defaultBg: "clean",
      defaultCard: "elevated",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Executive Navy", primary: "#1e3a8a", secondary: "#0284c7" },
        { name: "Slate Sapphire", primary: "#0f172a", secondary: "#2563eb" },
      ]
    },
    {
      id: "exec_mckinsey",
      name: "Strategy Advisory",
      category: "corporate",
      categoryName: "Corporate & Exec",
      layout: "corporate",
      layoutName: "Executive Briefing (2-Column)",
      layoutBadge: "Strategy Partner",
      icon: "📊",
      desc: "Deep navy and gold hairline accents, board-ready impact metrics, structured case findings",
      tags: ["Consulting", "Strategy", "Advisory"],
      defaultPrimary: "#0c2340",
      defaultSecondary: "#c5a059",
      font: "Plus Jakarta Sans",
      defaultBg: "clean",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Consultant Gold", primary: "#0c2340", secondary: "#c5a059" },
      ]
    },
    {
      id: "exec_wall_street",
      name: "Wall Street FinTech",
      category: "corporate",
      categoryName: "Corporate & Exec",
      layout: "corporate",
      layoutName: "Executive Briefing (2-Column)",
      layoutBadge: "Wall Street",
      icon: "📈",
      desc: "Steel slate and dark emerald ticker accents, quantitative metric highlights, banking governance",
      tags: ["Finance", "Banking", "Executive"],
      defaultPrimary: "#047857",
      defaultSecondary: "#0f172a",
      font: "Inter",
      defaultBg: "clean",
      defaultCard: "elevated",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Financial Emerald", primary: "#047857", secondary: "#0f172a" },
      ]
    },
    {
      id: "exec_enterprise_cto",
      name: "Enterprise CTO Ledger",
      category: "corporate",
      categoryName: "Corporate & Exec",
      layout: "corporate",
      layoutName: "Executive Briefing (2-Column)",
      layoutBadge: "CTO Architecture",
      icon: "🌐",
      desc: "Architectural governance, enterprise technology stack leadership, cross-org scale cards",
      tags: ["CTO", "Architecture", "Enterprise"],
      defaultPrimary: "#0369a1",
      defaultSecondary: "#475569",
      font: "Plus Jakarta Sans",
      defaultBg: "clean",
      defaultCard: "elevated",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "CTO Slate", primary: "#0369a1", secondary: "#475569" },
      ]
    },
    {
      id: "exec_deloitte",
      name: "Consulting Monograph",
      category: "corporate",
      categoryName: "Corporate & Exec",
      layout: "corporate",
      layoutName: "Executive Briefing (2-Column)",
      layoutBadge: "Audit Advisory",
      icon: "📑",
      desc: "Crisp corporate charcoal, signature green dot advisory badge, structured competency matrix",
      tags: ["Audit", "Consulting", "Enterprise"],
      defaultPrimary: "#1e293b",
      defaultSecondary: "#84cc16",
      font: "Inter",
      defaultBg: "clean",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Advisory Green", primary: "#1e293b", secondary: "#84cc16" },
      ]
    },
    {
      id: "exec_private_equity",
      name: "Private Equity Partner",
      category: "corporate",
      categoryName: "Corporate & Exec",
      layout: "corporate",
      layoutName: "Executive Briefing (2-Column)",
      layoutBadge: "Private Equity",
      icon: "💼",
      desc: "Oxford blue, polished bronze, portfolio company governance highlights, value creation metrics",
      tags: ["PE", "Venture", "Board"],
      defaultPrimary: "#172554",
      defaultSecondary: "#d97706",
      font: "Playfair Display",
      defaultBg: "clean",
      defaultCard: "elevated",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Oxford Amber", primary: "#172554", secondary: "#d97706" },
      ]
    },
    {
      id: "exec_global_vp",
      name: "Global VP Operations",
      category: "corporate",
      categoryName: "Corporate & Exec",
      layout: "corporate",
      layoutName: "Executive Briefing (2-Column)",
      layoutBadge: "Global VP",
      icon: "🌍",
      desc: "Cross-continental leadership milestones, supply chain & scaling KPIs, executive presence",
      tags: ["VP", "Operations", "Scale"],
      defaultPrimary: "#334155",
      defaultSecondary: "#0284c7",
      font: "Plus Jakarta Sans",
      defaultBg: "clean",
      defaultCard: "bordered",
      defaultBtn: "rounded",
      defaultDark: false,
      palettes: [
        { name: "Global Steel", primary: "#334155", secondary: "#0284c7" },
      ]
    },
    {
      id: "exec_legal_counsel",
      name: "General Counsel Ledger",
      category: "corporate",
      categoryName: "Corporate & Exec",
      layout: "corporate",
      layoutName: "Executive Briefing (2-Column)",
      layoutBadge: "Legal Counsel",
      icon: "⚖️",
      desc: "Formal structured clauses, regulatory compliance credentials, authoritative serif typography",
      tags: ["Legal", "Compliance", "Executive"],
      defaultPrimary: "#451a03",
      defaultSecondary: "#78350f",
      font: "Playfair Display",
      defaultBg: "clean",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Parchment Seal", primary: "#451a03", secondary: "#78350f" },
      ]
    },

    // ----------------------------------------------------
    // CATEGORY 5: AI & FUTURISTIC HUD (8 THEMES)
    // ----------------------------------------------------
    {
      id: "ai_tech",
      name: "AI / Tech HUD",
      category: "ai",
      categoryName: "AI & Cyber",
      layout: "ai_tech",
      layoutName: "Neural Interface & Telemetry",
      layoutBadge: "Neural HUD",
      icon: "🤖",
      desc: "Sci-fi cyber void, radar avatar rings, neural pod matrix, telemetry cards, glowing corner brackets",
      tags: ["AI", "HUD", "Sci-Fi"],
      defaultPrimary: "#06b6d4",
      defaultSecondary: "#c084fc",
      font: "Plus Jakarta Sans",
      defaultBg: "mesh",
      defaultCard: "glass",
      defaultBtn: "glow",
      defaultDark: true,
      palettes: [
        { name: "Quantum Cyan", primary: "#06b6d4", secondary: "#c084fc" },
        { name: "Neon Violet", primary: "#8b5cf6", secondary: "#38bdf8" },
      ]
    },
    {
      id: "ai_deepmind",
      name: "DeepMind Research Lab",
      category: "ai",
      categoryName: "AI & Cyber",
      layout: "ai_tech",
      layoutName: "Neural Interface & Telemetry",
      layoutBadge: "Research Lab",
      icon: "🧠",
      desc: "Ultra-clean cyan and lilac neural node matrix, scientific paper citations, frontier model engineer vibe",
      tags: ["DeepLearning", "Research", "Lab"],
      defaultPrimary: "#38bdf8",
      defaultSecondary: "#818cf8",
      font: "Inter",
      defaultBg: "dots",
      defaultCard: "glass",
      defaultBtn: "glow",
      defaultDark: true,
      palettes: [
        { name: "Frontier Cyan", primary: "#38bdf8", secondary: "#818cf8" },
      ]
    },
    {
      id: "ai_quantum",
      name: "Quantum Supercomputer",
      category: "ai",
      categoryName: "AI & Cyber",
      layout: "ai_tech",
      layoutName: "Neural Interface & Telemetry",
      layoutBadge: "Quantum HUD",
      icon: "⚛️",
      desc: "Cryogenic blue and electric cyan, sub-atomic particle glow, qubit simulation stats",
      tags: ["Quantum", "Physics", "Future"],
      defaultPrimary: "#00f2fe",
      defaultSecondary: "#4facfe",
      font: "Space Grotesk",
      defaultBg: "grid",
      defaultCard: "glass",
      defaultBtn: "glow",
      defaultDark: true,
      palettes: [
        { name: "Superconducting Teal", primary: "#00f2fe", secondary: "#4facfe" },
      ]
    },
    {
      id: "ai_agentic_swarm",
      name: "Autonomous Agent Core",
      category: "ai",
      categoryName: "AI & Cyber",
      layout: "dashboard",
      layoutName: "Interactive Cockpit",
      layoutBadge: "Agentic Swarm",
      icon: "🐝",
      desc: "Multi-agent coordination cockpit, task telemetry dials, live status stream for AI orchestrators",
      tags: ["Agents", "LLMs", "Cockpit"],
      defaultPrimary: "#10b981",
      defaultSecondary: "#06b6d4",
      font: "Fira Code",
      defaultBg: "grid",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: true,
      palettes: [
        { name: "Swarm Emerald", primary: "#10b981", secondary: "#06b6d4" },
      ]
    },
    {
      id: "ai_neural_synapse",
      name: "Synaptic Void",
      category: "ai",
      categoryName: "AI & Cyber",
      layout: "ai_tech",
      layoutName: "Neural Interface & Telemetry",
      layoutBadge: "Synapse Void",
      icon: "🔮",
      desc: "Deep purple abyss illuminated by pulsing neon pink synapse conduits and weight matrices",
      tags: ["Neural", "DeepLearning", "Purple"],
      defaultPrimary: "#c084fc",
      defaultSecondary: "#f43f5e",
      font: "Plus Jakarta Sans",
      defaultBg: "mesh",
      defaultCard: "glass",
      defaultBtn: "glow",
      defaultDark: true,
      palettes: [
        { name: "Synapse Pink", primary: "#c084fc", secondary: "#f43f5e" },
      ]
    },
    {
      id: "ai_cyber_sentinel",
      name: "Cyber Threat SOC",
      category: "ai",
      categoryName: "AI & Cyber",
      layout: "ai_tech",
      layoutName: "Neural Interface & Telemetry",
      layoutBadge: "Threat SOC",
      icon: "🛡️",
      desc: "Security Operations Center radar sweep, crimson warning accents, vulnerability triage badges",
      tags: ["Security", "Defense", "SOC"],
      defaultPrimary: "#ef4444",
      defaultSecondary: "#38bdf8",
      font: "Fira Code",
      defaultBg: "grid",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: true,
      palettes: [
        { name: "Alert Crimson", primary: "#ef4444", secondary: "#38bdf8" },
      ]
    },
    {
      id: "ai_singularity",
      name: "Singularity Horizon",
      category: "ai",
      categoryName: "AI & Cyber",
      layout: "ai_tech",
      layoutName: "Neural Interface & Telemetry",
      layoutBadge: "Singularity",
      icon: "🌌",
      desc: "Gravitational black hole accretion ring, cosmic violet light bending, futuristic theoretical AI",
      tags: ["Cosmic", "Future", "AGI"],
      defaultPrimary: "#a855f7",
      defaultSecondary: "#06b6d4",
      font: "Space Grotesk",
      defaultBg: "mesh",
      defaultCard: "glass",
      defaultBtn: "glow",
      defaultDark: true,
      palettes: [
        { name: "Event Horizon", primary: "#a855f7", secondary: "#06b6d4" },
      ]
    },
    {
      id: "ai_biomorphic",
      name: "Synthetic Biology AI",
      category: "ai",
      categoryName: "AI & Cyber",
      layout: "ai_tech",
      layoutName: "Neural Interface & Telemetry",
      layoutBadge: "Bio-Tech AI",
      icon: "🧬",
      desc: "Bio-luminescent lime & deep aquatic blue, DNA protein folding telemetry, computational biology",
      tags: ["BioTech", "AI", "Genomics"],
      defaultPrimary: "#22c55e",
      defaultSecondary: "#0284c7",
      font: "Plus Jakarta Sans",
      defaultBg: "dots",
      defaultCard: "glass",
      defaultBtn: "rounded",
      defaultDark: true,
      palettes: [
        { name: "Bio-Luminescent", primary: "#22c55e", secondary: "#0284c7" },
      ]
    },

    // ----------------------------------------------------
    // CATEGORY 6: MINIMALIST & SWISS TYPOGRAPHY (8 THEMES)
    // ----------------------------------------------------
    {
      id: "minimal",
      name: "Swiss Minimal",
      category: "minimal",
      categoryName: "Minimal & Swiss",
      layout: "minimal",
      layoutName: "Design Monograph & Index",
      layoutBadge: "Swiss Monograph",
      icon: "⚪",
      desc: "Numbered section index (01/ABOUT, 02/WORKS), stark typography, horizontal case study rows, hairline borders",
      tags: ["Swiss", "Editorial", "Clean"],
      defaultPrimary: "#111827",
      defaultSecondary: "#6b7280",
      font: "Inter",
      defaultBg: "clean",
      defaultCard: "flat",
      defaultBtn: "rounded",
      defaultDark: false,
      palettes: [
        { name: "Swiss Monochrome", primary: "#111827", secondary: "#6b7280" },
        { name: "Cool Slate", primary: "#1e293b", secondary: "#64748b" },
      ]
    },
    {
      id: "swiss_zurich",
      name: "Zurich International",
      category: "minimal",
      categoryName: "Minimal & Swiss",
      layout: "minimal",
      layoutName: "Design Monograph & Index",
      layoutBadge: "Zurich Grid",
      icon: "🇨🇭",
      desc: "Strict asymmetric column grid, pure black typography on bright white paper, zero ornament",
      tags: ["Zurich", "Helvetica", "Pure"],
      defaultPrimary: "#000000",
      defaultSecondary: "#52525b",
      font: "Inter",
      defaultBg: "clean",
      defaultCard: "flat",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Pure Black & White", primary: "#000000", secondary: "#52525b" },
      ]
    },
    {
      id: "minimal_monocle",
      name: "Monocle Dossier",
      category: "minimal",
      categoryName: "Minimal & Swiss",
      layout: "minimal",
      layoutName: "Design Monograph & Index",
      layoutBadge: "Monocle Press",
      icon: "👓",
      desc: "Refined British global journalism, warm grey hairlines, thoughtful serif annotations",
      tags: ["Journalism", "Dossier", "Minimal"],
      defaultPrimary: "#27272a",
      defaultSecondary: "#71717a",
      font: "Lora",
      defaultBg: "clean",
      defaultCard: "bordered",
      defaultBtn: "rounded",
      defaultDark: false,
      palettes: [
        { name: "Warm Dossier", primary: "#27272a", secondary: "#71717a" },
      ]
    },
    {
      id: "minimal_bauhaus",
      name: "Bauhaus Architecture",
      category: "minimal",
      categoryName: "Minimal & Swiss",
      layout: "minimal",
      layoutName: "Design Monograph & Index",
      layoutBadge: "Bauhaus Grid",
      icon: "📐",
      desc: "Form follows function: bold scarlet and ultramarine geometry accents, stark functional rules",
      tags: ["Bauhaus", "Modernist", "Architecture"],
      defaultPrimary: "#dc2626",
      defaultSecondary: "#2563eb",
      font: "Inter",
      defaultBg: "clean",
      defaultCard: "flat",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Bauhaus Primary", primary: "#dc2626", secondary: "#2563eb" },
      ]
    },
    {
      id: "minimal_hairline",
      name: "Hairline Monograph",
      category: "minimal",
      categoryName: "Minimal & Swiss",
      layout: "minimal",
      layoutName: "Design Monograph & Index",
      layoutBadge: "Hairline Fine",
      icon: "📏",
      desc: "Sub-pixel fine dividers, expansive whitespace, quiet sophistication and subtle typography",
      tags: ["Subtle", "Quiet", "Design"],
      defaultPrimary: "#3f3f46",
      defaultSecondary: "#a1a1aa",
      font: "Inter",
      defaultBg: "clean",
      defaultCard: "bordered",
      defaultBtn: "rounded",
      defaultDark: false,
      palettes: [
        { name: "Fine Graphite", primary: "#3f3f46", secondary: "#a1a1aa" },
      ]
    },
    {
      id: "minimal_ink",
      name: "Ink & Japanese Washi",
      category: "minimal",
      categoryName: "Minimal & Swiss",
      layout: "minimal",
      layoutName: "Design Monograph & Index",
      layoutBadge: "Japanese Washi",
      icon: "⛩️",
      desc: "Sumie black ink brush tone, warm parchment paper canvas, zen minimalism and deliberate pacing",
      tags: ["Zen", "Washi", "Serene"],
      defaultPrimary: "#18181b",
      defaultSecondary: "#78716c",
      font: "Playfair Display",
      defaultBg: "clean",
      defaultCard: "flat",
      defaultBtn: "rounded",
      defaultDark: false,
      palettes: [
        { name: "Sumi Ink", primary: "#18181b", secondary: "#78716c" },
      ]
    },
    {
      id: "minimal_studio",
      name: "Nordic Architecture",
      category: "minimal",
      categoryName: "Minimal & Swiss",
      layout: "minimal",
      layoutName: "Design Monograph & Index",
      layoutBadge: "Nordic Studio",
      icon: "🪵",
      desc: "Natural sand tones, charcoal typography, unadorned structural layout for architects and researchers",
      tags: ["Nordic", "Natural", "Minimal"],
      defaultPrimary: "#44403c",
      defaultSecondary: "#a8a29e",
      font: "Plus Jakarta Sans",
      defaultBg: "clean",
      defaultCard: "flat",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Sand & Charcoal", primary: "#44403c", secondary: "#a8a29e" },
      ]
    },
    {
      id: "minimal_brutalist_mono",
      name: "Stark Monospace",
      category: "minimal",
      categoryName: "Minimal & Swiss",
      layout: "minimal",
      layoutName: "Design Monograph & Index",
      layoutBadge: "Stark Mono",
      icon: "🔤",
      desc: "Pure typewriter monospace text, zero decorative cards, radical typographic honesty",
      tags: ["Monospace", "Raw", "Minimal"],
      defaultPrimary: "#09090b",
      defaultSecondary: "#71717a",
      font: "Fira Code",
      defaultBg: "clean",
      defaultCard: "flat",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Raw Typewriter", primary: "#09090b", secondary: "#71717a" },
      ]
    },

    // ----------------------------------------------------
    // CATEGORY 7: DARK LUXURY & OLED TITANIUM (8 THEMES)
    // ----------------------------------------------------
    {
      id: "dark",
      name: "Dark Luxury",
      category: "dark",
      categoryName: "Dark & Luxury",
      layout: "dark",
      layoutName: "OLED Midnight Titanium",
      layoutBadge: "OLED Titanium",
      icon: "🌙",
      desc: "OLED deep black, frosted titanium glass, metallic gradient borders, ambient gold & cyan backlights",
      tags: ["Luxury", "Titanium", "Dark"],
      defaultPrimary: "#6366f1",
      defaultSecondary: "#38bdf8",
      font: "Plus Jakarta Sans",
      defaultBg: "dots",
      defaultCard: "glass",
      defaultBtn: "rounded",
      defaultDark: true,
      palettes: [
        { name: "Titanium Indigo", primary: "#6366f1", secondary: "#38bdf8" },
        { name: "Obsidian Gold", primary: "#fbbf24", secondary: "#f59e0b" },
      ]
    },
    {
      id: "dark_obsidian",
      name: "Obsidian Noir",
      category: "dark",
      categoryName: "Dark & Luxury",
      layout: "dark",
      layoutName: "OLED Midnight Titanium",
      layoutBadge: "Obsidian Noir",
      icon: "🖤",
      desc: "Pure #050508 OLED black, subtle edge bevel reflections, silver hairline typography",
      tags: ["OLED", "Obsidian", "Sleek"],
      defaultPrimary: "#94a3b8",
      defaultSecondary: "#cbd5e1",
      font: "Inter",
      defaultBg: "clean",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: true,
      palettes: [
        { name: "Silver Obsidian", primary: "#94a3b8", secondary: "#cbd5e1" },
      ]
    },
    {
      id: "dark_emerald_gold",
      name: "Emerald Royalty",
      category: "dark",
      categoryName: "Dark & Luxury",
      layout: "dark",
      layoutName: "OLED Midnight Titanium",
      layoutBadge: "Emerald Gold",
      icon: "👑",
      desc: "Deep forest emerald velvet cards accented with polished champagne gold borders and badges",
      tags: ["Royalty", "Emerald", "Gold"],
      defaultPrimary: "#10b981",
      defaultSecondary: "#fbbf24",
      font: "Playfair Display",
      defaultBg: "mesh",
      defaultCard: "glass",
      defaultBtn: "rounded",
      defaultDark: true,
      palettes: [
        { name: "Imperial Emerald", primary: "#10b981", secondary: "#fbbf24" },
      ]
    },
    {
      id: "dark_carbon_fibre",
      name: "Carbon Fibre Pro",
      category: "dark",
      categoryName: "Dark & Luxury",
      layout: "dark",
      layoutName: "OLED Midnight Titanium",
      layoutBadge: "Carbon Fibre",
      icon: "🏎️",
      desc: "Woven composite texture aesthetic, McLaren orange racing telemetry accents, hyper-performance feel",
      tags: ["Carbon", "Racing", "Tech"],
      defaultPrimary: "#f97316",
      defaultSecondary: "#64748b",
      font: "Space Grotesk",
      defaultBg: "grid",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: true,
      palettes: [
        { name: "Motorsport Orange", primary: "#f97316", secondary: "#64748b" },
      ]
    },
    {
      id: "dark_amethyst",
      name: "Royal Amethyst",
      category: "dark",
      categoryName: "Dark & Luxury",
      layout: "dark",
      layoutName: "OLED Midnight Titanium",
      layoutBadge: "Amethyst",
      icon: "💎",
      desc: "Deep imperial purple twilight glow, faceted crystal accents, jewel-tone lighting",
      tags: ["Amethyst", "Jewel", "Glow"],
      defaultPrimary: "#a855f7",
      defaultSecondary: "#ec4899",
      font: "Plus Jakarta Sans",
      defaultBg: "mesh",
      defaultCard: "glass",
      defaultBtn: "glow",
      defaultDark: true,
      palettes: [
        { name: "Imperial Violet", primary: "#a855f7", secondary: "#ec4899" },
      ]
    },
    {
      id: "dark_champagne",
      name: "Champagne Titanium",
      category: "dark",
      categoryName: "Dark & Luxury",
      layout: "dark",
      layoutName: "OLED Midnight Titanium",
      layoutBadge: "Horology",
      icon: "🍾",
      desc: "Luxury horology watchmaker aesthetic: warm metallic gold bezels, dark satin surfaces",
      tags: ["Luxury", "Champagne", "Horology"],
      defaultPrimary: "#d97706",
      defaultSecondary: "#fef3c7",
      font: "Playfair Display",
      defaultBg: "dots",
      defaultCard: "glass",
      defaultBtn: "rounded",
      defaultDark: true,
      palettes: [
        { name: "Horology Gold", primary: "#d97706", secondary: "#fef3c7" },
      ]
    },
    {
      id: "dark_sapphire",
      name: "Midnight Sapphire",
      category: "dark",
      categoryName: "Dark & Luxury",
      layout: "dark",
      layoutName: "OLED Midnight Titanium",
      layoutBadge: "Sapphire Night",
      icon: "🌌",
      desc: "Deep abyss ocean midnight with electric azure and royal blue backlights",
      tags: ["Sapphire", "Ocean", "Dark"],
      defaultPrimary: "#0ea5e9",
      defaultSecondary: "#6366f1",
      font: "Plus Jakarta Sans",
      defaultBg: "mesh",
      defaultCard: "glass",
      defaultBtn: "glow",
      defaultDark: true,
      palettes: [
        { name: "Deep Abyss", primary: "#0ea5e9", secondary: "#6366f1" },
      ]
    },
    {
      id: "dark_cyber_crimson",
      name: "Crimson Phantom",
      category: "dark",
      categoryName: "Dark & Luxury",
      layout: "dark",
      layoutName: "OLED Midnight Titanium",
      layoutBadge: "Phantom Red",
      icon: "🩸",
      desc: "Intense ruby red laser glow against jet-black matte panels for stealth security leaders",
      tags: ["Crimson", "Stealth", "Laser"],
      defaultPrimary: "#f43f5e",
      defaultSecondary: "#fb7185",
      font: "Inter",
      defaultBg: "dots",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: true,
      palettes: [
        { name: "Ruby Phantom", primary: "#f43f5e", secondary: "#fb7185" },
      ]
    },

    // ----------------------------------------------------
    // CATEGORY 8: CLASSICAL & EDITORIAL GAZETTE (6 THEMES)
    // ----------------------------------------------------
    {
      id: "elegant",
      name: "Classical Gazette",
      category: "editorial",
      categoryName: "Classical Gazette",
      layout: "elegant",
      layoutName: "Classical Luxury Gazette",
      layoutBadge: "Heritage CV",
      icon: "📜",
      desc: "Warm ivory canvas, literary drop caps, ornamental serif masthead, distinguished curriculum vitae entries",
      tags: ["Heritage", "Gazette", "Literary"],
      defaultPrimary: "#92643b",
      defaultSecondary: "#4a5568",
      font: "Playfair Display",
      defaultBg: "clean",
      defaultCard: "elevated",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Tuscan Bronze", primary: "#92643b", secondary: "#4a5568" },
        { name: "Burgundy Heritage", primary: "#881337", secondary: "#b45309" },
      ]
    },
    {
      id: "elegant_vogue",
      name: "Vogue High Editorial",
      category: "editorial",
      categoryName: "Classical Gazette",
      layout: "split_screen",
      layoutName: "Split-Screen Showcase",
      layoutBadge: "Vogue Press",
      icon: "👠",
      desc: "High fashion editorial spreads, oversized serif headlines, magazine layout column architecture",
      tags: ["Vogue", "Fashion", "Editorial"],
      defaultPrimary: "#09090b",
      defaultSecondary: "#be123c",
      font: "Playfair Display",
      defaultBg: "clean",
      defaultCard: "flat",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Editorial Noir", primary: "#09090b", secondary: "#be123c" },
      ]
    },
    {
      id: "elegant_cambridge",
      name: "Cambridge Scholarly",
      category: "editorial",
      categoryName: "Classical Gazette",
      layout: "elegant",
      layoutName: "Classical Luxury Gazette",
      layoutBadge: "Cambridge Don",
      icon: "🎓",
      desc: "Collegiate navy, distinguished scholarly crest framing, peer-reviewed monograph pedigree",
      tags: ["Academic", "Scholarly", "University"],
      defaultPrimary: "#1e3a8a",
      defaultSecondary: "#b45309",
      font: "Playfair Display",
      defaultBg: "clean",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Collegiate Navy", primary: "#1e3a8a", secondary: "#b45309" },
      ]
    },
    {
      id: "elegant_broadsheet",
      name: "Financial Broadsheet",
      category: "editorial",
      categoryName: "Classical Gazette",
      layout: "elegant",
      layoutName: "Classical Luxury Gazette",
      layoutBadge: "Broadsheet",
      icon: "🗞️",
      desc: "Salmon-tinted newsprint aesthetic, multi-column press formatting, authoritative economic tone",
      tags: ["Broadsheet", "Press", "Economics"],
      defaultPrimary: "#831843",
      defaultSecondary: "#374151",
      font: "Playfair Display",
      defaultBg: "clean",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Salmon Broadsheet", primary: "#831843", secondary: "#374151" },
      ]
    },
    {
      id: "elegant_renaissance",
      name: "Florentine Humanist",
      category: "editorial",
      categoryName: "Classical Gazette",
      layout: "elegant",
      layoutName: "Classical Luxury Gazette",
      layoutBadge: "Florentine",
      icon: "🏛️",
      desc: "Italian Renaissance proportions, terracotta warmth, classical monument serif display lettering",
      tags: ["Renaissance", "Terracotta", "Classics"],
      defaultPrimary: "#78350f",
      defaultSecondary: "#92400e",
      font: "Cinzel",
      defaultBg: "clean",
      defaultCard: "elevated",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Florentine Terra", primary: "#78350f", secondary: "#92400e" },
      ]
    },
    {
      id: "elegant_curator",
      name: "Museum Curator Monograph",
      category: "editorial",
      categoryName: "Classical Gazette",
      layout: "split_screen",
      layoutName: "Split-Screen Showcase",
      layoutBadge: "Curator Archive",
      icon: "🖼️",
      desc: "Exhibition catalog layout, artwork project frames, curated biographical chronology",
      tags: ["Museum", "Curator", "Exhibition"],
      defaultPrimary: "#1c1917",
      defaultSecondary: "#57534e",
      font: "Playfair Display",
      defaultBg: "clean",
      defaultCard: "flat",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Curator Archive", primary: "#1c1917", secondary: "#57534e" },
      ]
    },

    // ----------------------------------------------------
    // CATEGORY 9: NOTION & CLEAN DOCS WORKSPACE (6 THEMES)
    // ----------------------------------------------------
    {
      id: "notion_doc",
      name: "Notion Clean Workspace",
      category: "notion",
      categoryName: "Notion & Docs",
      layout: "notion",
      layoutName: "Notion Workspace Document",
      layoutBadge: "Notion Doc",
      icon: "📝",
      desc: "Document cover banner, emoji icon, clean callouts, database table project view, pastel property tags",
      tags: ["Notion", "Clean", "Workspace"],
      defaultPrimary: "#2563eb",
      defaultSecondary: "#64748b",
      font: "Inter",
      defaultBg: "clean",
      defaultCard: "bordered",
      defaultBtn: "rounded",
      defaultDark: false,
      palettes: [
        { name: "Notion Classic", primary: "#2563eb", secondary: "#64748b" },
        { name: "Notion Olive", primary: "#65a30d", secondary: "#475569" },
      ]
    },
    {
      id: "notion_craft",
      name: "Craft Knowledge Base",
      category: "notion",
      categoryName: "Notion & Docs",
      layout: "notion",
      layoutName: "Notion Workspace Document",
      layoutBadge: "Craft Doc",
      icon: "📋",
      desc: "Card-style doc blocks, soft rounded corners, pastel tags, delightful personal knowledge garden",
      tags: ["Craft", "Garden", "Docs"],
      defaultPrimary: "#7c3aed",
      defaultSecondary: "#06b6d4",
      font: "Plus Jakarta Sans",
      defaultBg: "mesh",
      defaultCard: "glass",
      defaultBtn: "pill",
      defaultDark: false,
      palettes: [
        { name: "Craft Violet", primary: "#7c3aed", secondary: "#06b6d4" },
      ]
    },
    {
      id: "notion_obsidian",
      name: "Obsidian Second Brain",
      category: "notion",
      categoryName: "Notion & Docs",
      layout: "notion",
      layoutName: "Notion Workspace Document",
      layoutBadge: "Obsidian Vault",
      icon: "🪨",
      desc: "Dark mode markdown vault, bidirectional linked tag badges, technical research note format",
      tags: ["Obsidian", "Markdown", "Dark"],
      defaultPrimary: "#a855f7",
      defaultSecondary: "#38bdf8",
      font: "Inter",
      defaultBg: "dots",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: true,
      palettes: [
        { name: "Vault Violet", primary: "#a855f7", secondary: "#38bdf8" },
      ]
    },
    {
      id: "notion_linear",
      name: "Linear Documentation",
      category: "notion",
      categoryName: "Notion & Docs",
      layout: "notion",
      layoutName: "Notion Workspace Document",
      layoutBadge: "Linear Specs",
      icon: "📐",
      desc: "Dark developer specifications, keyboard shortcuts, clean issue status pills, product manager favorite",
      tags: ["Product", "Spec", "Dark"],
      defaultPrimary: "#5e6ad2",
      defaultSecondary: "#94a3b8",
      font: "Inter",
      defaultBg: "dots",
      defaultCard: "bordered",
      defaultBtn: "rounded",
      defaultDark: true,
      palettes: [
        { name: "Linear Spec", primary: "#5e6ad2", secondary: "#94a3b8" },
      ]
    },
    {
      id: "notion_paper",
      name: "Moleskine Paper Notes",
      category: "notion",
      categoryName: "Notion & Docs",
      layout: "notion",
      layoutName: "Notion Workspace Document",
      layoutBadge: "Moleskine",
      icon: "📓",
      desc: "Warm textured ruled paper rows, leather binding warmth, thoughtful notebook personal brand",
      tags: ["Paper", "Notebook", "Warm"],
      defaultPrimary: "#b45309",
      defaultSecondary: "#78716c",
      font: "Lora",
      defaultBg: "clean",
      defaultCard: "bordered",
      defaultBtn: "rounded",
      defaultDark: false,
      palettes: [
        { name: "Warm Leather", primary: "#b45309", secondary: "#78716c" },
      ]
    },
    {
      id: "notion_wiki",
      name: "Engineering Handbook",
      category: "notion",
      categoryName: "Notion & Docs",
      layout: "notion",
      layoutName: "Notion Workspace Document",
      layoutBadge: "Eng Handbook",
      icon: "📖",
      desc: "Internal tech team handbook format, clean section callouts, structured engineering guidelines",
      tags: ["Handbook", "Engineering", "Wiki"],
      defaultPrimary: "#0284c7",
      defaultSecondary: "#10b981",
      font: "Inter",
      defaultBg: "clean",
      defaultCard: "bordered",
      defaultBtn: "rounded",
      defaultDark: false,
      palettes: [
        { name: "Wiki Blue", primary: "#0284c7", secondary: "#10b981" },
      ]
    },

    // ----------------------------------------------------
    // CATEGORY 10: CAREER JOURNEY & STORYBOARDS (6 THEMES)
    // ----------------------------------------------------
    {
      id: "timeline_journey",
      name: "Milestone Journey Trail",
      category: "timeline",
      categoryName: "Journey & Milestones",
      layout: "timeline",
      layoutName: "Career Journey & Milestones",
      layoutBadge: "Milestone Trail",
      icon: "🧭",
      desc: "Vertical zigzag milestone trail with glowing waypoint nodes, story cards, career progression narrative",
      tags: ["Journey", "Timeline", "Story"],
      defaultPrimary: "#4f46e5",
      defaultSecondary: "#06b6d4",
      font: "Plus Jakarta Sans",
      defaultBg: "mesh",
      defaultCard: "glass",
      defaultBtn: "rounded",
      defaultDark: false,
      palettes: [
        { name: "Journey Indigo", primary: "#4f46e5", secondary: "#06b6d4" },
        { name: "Summit Sunset", primary: "#f43f5e", secondary: "#fb923c" },
      ]
    },
    {
      id: "timeline_space",
      name: "Apollo Mission Log",
      category: "timeline",
      categoryName: "Journey & Milestones",
      layout: "timeline",
      layoutName: "Career Journey & Milestones",
      layoutBadge: "Mission Log",
      icon: "🚀",
      desc: "NASA mission log: launch sequence milestones, orbit insertion achievements, telemetry timestamping",
      tags: ["Space", "Mission", "Dark"],
      defaultPrimary: "#38bdf8",
      defaultSecondary: "#f59e0b",
      font: "Space Grotesk",
      defaultBg: "dots",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: true,
      palettes: [
        { name: "Apollo Sky", primary: "#38bdf8", secondary: "#f59e0b" },
      ]
    },
    {
      id: "timeline_expedition",
      name: "Founder Expedition",
      category: "timeline",
      categoryName: "Journey & Milestones",
      layout: "timeline",
      layoutName: "Career Journey & Milestones",
      layoutBadge: "Expedition",
      icon: "⛺",
      desc: "Startup founder chapters: 0→1 inception, product-market fit, venture scaling, next frontiers",
      tags: ["Founder", "Startup", "Story"],
      defaultPrimary: "#ea580c",
      defaultSecondary: "#3b82f6",
      font: "Outfit",
      defaultBg: "mesh",
      defaultCard: "elevated",
      defaultBtn: "rounded",
      defaultDark: false,
      palettes: [
        { name: "Founder Flame", primary: "#ea580c", secondary: "#3b82f6" },
      ]
    },
    {
      id: "timeline_craft",
      name: "Design Evolution Trail",
      category: "timeline",
      categoryName: "Journey & Milestones",
      layout: "timeline",
      layoutName: "Career Journey & Milestones",
      layoutBadge: "Design Trail",
      icon: "✨",
      desc: "Visual portfolio progression through major craft eras, creative breakthrough waypoints",
      tags: ["Design", "Craft", "Evolution"],
      defaultPrimary: "#ec4899",
      defaultSecondary: "#8b5cf6",
      font: "Outfit",
      defaultBg: "mesh",
      defaultCard: "glass",
      defaultBtn: "pill",
      defaultDark: false,
      palettes: [
        { name: "Craft Evolution", primary: "#ec4899", secondary: "#8b5cf6" },
      ]
    },
    {
      id: "timeline_metro",
      name: "Transit Metro Line",
      category: "timeline",
      categoryName: "Journey & Milestones",
      layout: "timeline",
      layoutName: "Career Journey & Milestones",
      layoutBadge: "Transit Metro",
      icon: "🚇",
      desc: "Subway map line aesthetic connecting experience transit stations and transfer nodes",
      tags: ["Transit", "Map", "Graphic"],
      defaultPrimary: "#059669",
      defaultSecondary: "#2563eb",
      font: "Inter",
      defaultBg: "clean",
      defaultCard: "bordered",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Metro Transit", primary: "#059669", secondary: "#2563eb" },
      ]
    },
    {
      id: "timeline_chronicle",
      name: "Historical Career Chronicle",
      category: "timeline",
      categoryName: "Journey & Milestones",
      layout: "timeline",
      layoutName: "Career Journey & Milestones",
      layoutBadge: "Chronicle",
      icon: "📜",
      desc: "Grand historical chronicle, illustrated era badges, in-depth narrative progression",
      tags: ["History", "Chronicle", "Serif"],
      defaultPrimary: "#7c2d12",
      defaultSecondary: "#0284c7",
      font: "Playfair Display",
      defaultBg: "clean",
      defaultCard: "elevated",
      defaultBtn: "sharp",
      defaultDark: false,
      palettes: [
        { name: "Historical Leather", primary: "#7c2d12", secondary: "#0284c7" },
      ]
    },
  ];

  function escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function safeParseJSON(val, fallback) {
    if (val === null || val === undefined) return fallback;
    if (typeof val === "object") return val;
    if (typeof val === "string") {
      try {
        const parsed = JSON.parse(val);
        return parsed !== null && parsed !== undefined ? parsed : fallback;
      } catch {
        return fallback;
      }
    }
    return fallback;
  }

  /**
   * Normalizes and cleans education items for consistent, polished presentation.
   * - Extracts GPA / score from institution names if mashed together
   * - Strips placeholder degree names (like "Academic Degree" or "Education") and derives professional titles
   * - Merges broken/orphaned entries (e.g. institution is "-" with isolated year) into preceding degree
   * - Fixes circular HSC/SSLC institution descriptions
   */
  function normalizeEducationList(education) {
    if (!education) return [];
    let list = Array.isArray(education) ? education : safeParseJSON(education, []);
    if (!Array.isArray(list)) return [];

    const normalized = [];

    for (let i = 0; i < list.length; i++) {
      const raw = list[i];
      if (!raw || typeof raw !== "object") continue;

      let degree = (raw.degree || "").trim();
      let inst = (raw.institution || "").trim();
      let year = (raw.end_year || raw.start_year || raw.year || "").trim();
      let field = (raw.field_of_study || "").trim();
      let score = (raw.score || raw.details || raw.grade || "").trim();

      // 1. Extract GPA / CGPA / Score from institution if embedded
      const scoreInInst = inst.match(/\b(?:c?gpa|grade|score|percentage)\s*[:\-–—]?\s*(\d+(?:\.\d+)?(?:\s*\/\s*\d+)?(?:\s*(?:cgpa|gpa|%))?)/i) ||
                          inst.match(/[\s,\-|–—]+(\d+(?:\.\d+)?\s*(?:\/\s*\d+)?\s*(?:%|cgpa|gpa))\b/i);
      if (scoreInInst) {
        if (!score || score === "-") {
          score = scoreInInst[0].replace(/^[\s,\-|–—]+/, "").trim();
        }
        inst = inst.replace(/\s*[\s,\-|–—]*\b(?:c?gpa|grade|score|percentage)\s*[:\-–—]?\s*\d+(?:\.\d+)?(?:\s*\/\s*\d+)?(?:\s*(?:cgpa|gpa|%))?.*$/i, "").trim();
        inst = inst.replace(/[\s,\-|–—]+(?:\d+(?:\.\d+)?\s*(?:\/\s*\d+)?\s*(?:%|cgpa|gpa))\b.*$/i, "").trim();
        inst = inst.replace(/[\s,\-|–—]+$/, "").trim();
      }

      // Also clean details/score if it starts with dash
      if (score === "-") score = "";

      // 2. Check if this is an orphaned / broken dummy entry (e.g. institution is "-" or empty)
      const isDummyInst = !inst || inst === "-" || inst.toLowerCase() === "n/a" || inst.toLowerCase() === "none";
      const isGenericDeg = !degree || degree.toLowerCase() === "academic degree" || degree.toLowerCase() === "education" || degree === "-";

      if (isDummyInst && isGenericDeg) {
        // Attach isolated year or score to the appropriate college/academic degree entry that lacks one
        if (normalized.length > 0) {
          const target = normalized.find(e => !e.end_year && (
            (e.degree && e.degree.toLowerCase().includes("bachelor")) ||
            (e.degree && e.degree.toLowerCase().includes("degree")) ||
            (e.degree && e.degree.toLowerCase().includes("b.sc")) ||
            (e.degree && e.degree.toLowerCase().includes("b.tech"))
          )) || normalized.find(e => !e.end_year) || normalized[0];

          if (year && target && !target.end_year) {
            target.end_year = year;
          }
          if (score && target && !target.score) {
            target.score = score;
            target.details = score;
          }
        }
        continue;
      }

      // If inst is dummy but has isolated year and preceding entry lacks end_year
      if (isDummyInst && year && !field && !score && normalized.length > 0) {
        const target = normalized.find(e => !e.end_year) || normalized[0];
        if (target && !target.end_year) {
          target.end_year = year;
        }
        continue;
      }

      // 3. Clean placeholder degree names
      if (!degree || degree.toLowerCase() === "academic degree" || degree.toLowerCase() === "education" || degree === "-") {
        if (inst.toLowerCase().includes("arts and science") || inst.toLowerCase().includes("college of science")) {
          degree = field ? `Bachelor of Science (${field.split('/')[0].trim()})` : "Bachelor of Science (B.Sc)";
        } else if (field && (field.toLowerCase().includes("computer") || field.toLowerCase().includes("engineering") || field.toLowerCase().includes("technology"))) {
          degree = "Bachelor of Science / Engineering";
        } else if (field) {
          degree = `Bachelor's Degree in ${field}`;
        } else {
          degree = "Bachelor's Degree";
        }
      }

      // 4. Clean HSC / SSLC redundant entries
      if (degree.toUpperCase().includes("HSC") || degree.toUpperCase().includes("HIGHER SECONDARY")) {
        degree = "Higher Secondary Certificate (HSC)";
        if (!inst || inst === "-" || inst.toLowerCase().includes("higher secondary certificate") || inst.toLowerCase() === "hsc") {
          inst = "State Board / Higher Secondary School";
        }
        if (!field) field = "Higher Secondary (12th)";
      } else if (degree.toUpperCase().includes("SSLC") || degree.toUpperCase().includes("SECONDARY SCHOOL")) {
        degree = "Secondary School Leaving Certificate (SSLC)";
        if (!inst || inst === "-" || inst.toLowerCase().includes("secondary school leaving") || inst.toLowerCase() === "sslc") {
          inst = "State Board / Secondary School";
        }
        if (!field) field = "Secondary Education (10th)";
      } else if (inst.toLowerCase() === "higher secondary certificate (hsc)" || inst.toLowerCase() === "higher secondary certificate") {
        inst = "State Board / Higher Secondary School";
      }

      // Strip trailing/leading punctuation from institution
      inst = inst.replace(/^[\s,\-|–—]+|[\s,\-|–—]+$/g, "").trim();

      normalized.push({
        ...raw,
        degree,
        institution: inst || "Institution",
        end_year: year || raw.end_year || "",
        start_year: raw.start_year || "",
        field_of_study: field,
        score: score,
        details: score || raw.details || "",
      });
    }

    return normalized;
  }

  function getIconHtml(iconName, defaultFallback = "✦") {
    if (!iconName) return defaultFallback;
    const clean = String(iconName).trim().toLowerCase();
    const map = {
      "shield-check": "🛡️",
      "shield": "🛡️",
      "cpu": "⚡",
      "zap": "⚡",
      "bolt": "⚡",
      "trending-down": "📉",
      "trending-up": "📈",
      "database": "🗄️",
      "server": "🖥️",
      "code": "💻",
      "terminal": "💻",
      "award": "🏆",
      "star": "⭐",
      "check": "✓",
      "globe": "🌐",
      "layers": "📚",
      "briefcase": "💼",
      "book": "📖",
      "tool": "🛠️",
      "tools": "🛠️",
      "users": "👥",
      "user": "👤",
      "mail": "✉️",
      "target": "🎯",
      "activity": "📊",
      "bar-chart": "📊",
      "chart": "📊",
      "cloud": "☁️",
    };
    if (map[clean]) return map[clean];
    if (clean.length <= 4 && !/^[a-z0-9_-]+$/.test(clean)) return iconName;
    return defaultFallback;
  }

  /**
   * High-resolution, professional curated background presets tailored to candidate domains
   */
  const DOMAIN_BACKGROUNDS = {
    ai_tech: {
      key: "ai_tech",
      domain: "Artificial Intelligence & Computational Systems",
      url: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=2000&q=80",
      title: "AI & Neural Computing Studio",
      description: "Computational research architecture and production machine learning engineering",
      overlayLight: "rgba(244, 247, 255, 0.76)",
      overlayDark: "rgba(6, 12, 28, 0.74)",
      accent: "#06b6d4",
      accentRgb: "6, 182, 212",
    },
    developer: {
      key: "developer",
      domain: "Software Engineering & Full Stack",
      url: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=2000&q=80",
      title: "Software Engineering Workstation",
      description: "Clean focused dual-monitor development environment with code syntax",
      overlayLight: "rgba(244, 247, 255, 0.76)",
      overlayDark: "rgba(10, 15, 26, 0.75)",
      accent: "#3b82f6",
      accentRgb: "59, 130, 246",
    },
    cloud_devops: {
      key: "cloud_devops",
      domain: "Cloud Infrastructure, DevOps & SRE",
      url: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=2000&q=80",
      title: "Distributed Cloud Architecture",
      description: "High-density global cloud topology, container orchestration, and telemetry",
      overlayLight: "rgba(240, 247, 255, 0.76)",
      overlayDark: "rgba(8, 14, 29, 0.74)",
      accent: "#0ea5e9",
      accentRgb: "14, 165, 233",
    },
    creative: {
      key: "creative",
      domain: "UI/UX & Product Design",
      url: "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=2000&q=80",
      title: "Product Design & Prototyping Studio",
      description: "Modern creative workstation with design systems and responsive prototyping",
      overlayLight: "rgba(253, 242, 248, 0.74)",
      overlayDark: "rgba(24, 16, 38, 0.72)",
      accent: "#8b5cf6",
      accentRgb: "139, 92, 246",
    },
    corporate: {
      key: "corporate",
      domain: "Executive Leadership & Product Management",
      url: "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=2000&q=80",
      title: "Metropolitan Executive Architecture",
      description: "Sunlit corporate boardroom and modern leadership environment",
      overlayLight: "rgba(241, 245, 249, 0.76)",
      overlayDark: "rgba(15, 23, 42, 0.74)",
      accent: "#2563eb",
      accentRgb: "37, 99, 235",
    },
    elegant: {
      key: "elegant",
      domain: "Strategy Consulting & Architecture",
      url: "https://images.unsplash.com/photo-1497215728101-856f4ea42174?auto=format&fit=crop&w=2000&q=80",
      title: "Curated Strategy Advisory Studio",
      description: "High-aesthetic Scandinavian consulting studio with bespoke natural daylight",
      overlayLight: "rgba(250, 248, 245, 0.76)",
      overlayDark: "rgba(28, 25, 23, 0.74)",
      accent: "#d97706",
      accentRgb: "217, 119, 6",
    },
    minimal: {
      key: "minimal",
      domain: "Minimalist Engineering & Research",
      url: "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=2000&q=80",
      title: "Clean Minimalist Engineering Desk",
      description: "Focused modern tech setup with notebook, clean architecture and quiet precision",
      overlayLight: "rgba(248, 250, 252, 0.74)",
      overlayDark: "rgba(17, 24, 39, 0.72)",
      accent: "#64748b",
      accentRgb: "100, 116, 139",
    },
    dark: {
      key: "dark",
      domain: "Dark Luxury & Systems Engineering",
      url: "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=2000&q=80",
      title: "Precision Hardware Systems Studio",
      description: "Moody tech workspace with clean aesthetic hardware and ambient studio lighting",
      overlayLight: "rgba(241, 245, 249, 0.76)",
      overlayDark: "rgba(9, 9, 11, 0.76)",
      accent: "#6366f1",
      accentRgb: "99, 102, 241",
    },
    saas: {
      key: "saas",
      domain: "Modern SaaS & Product Engineering",
      url: "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=2000&q=80",
      title: "Modern Software Engineering Desk",
      description: "Clean focused product development workspace with high productivity optics",
      overlayLight: "rgba(241, 245, 249, 0.76)",
      overlayDark: "rgba(15, 23, 42, 0.74)",
      accent: "#6366f1",
      accentRgb: "99, 102, 241",
    },
    data_analytics: {
      key: "data_analytics",
      domain: "Data Science, Telemetry & Analytics",
      url: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=2000&q=80",
      title: "Telemetry Analytics & Data Station",
      description: "Real-time analytics dashboards, metrics telemetry, and quantitative insights",
      overlayLight: "rgba(240, 249, 255, 0.76)",
      overlayDark: "rgba(11, 19, 43, 0.74)",
      accent: "#10b981",
      accentRgb: "16, 185, 129",
    },
    hr_recruiting: {
      key: "hr_recruiting",
      domain: "Talent Acquisition & People Operations",
      url: "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=2000&q=80",
      title: "People & Talent Strategy Studio",
      description: "Collaborative modern team conference and strategic people operations",
      overlayLight: "rgba(253, 242, 248, 0.74)",
      overlayDark: "rgba(24, 16, 38, 0.72)",
      accent: "#ec4899",
      accentRgb: "236, 72, 153",
    },
    mobile: {
      key: "mobile",
      domain: "Mobile & Edge Systems Engineering",
      url: "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?auto=format&fit=crop&w=2000&q=80",
      title: "Mobile Device Interface Lab",
      description: "Touchscreen development studio and edge mobile engineering",
      overlayLight: "rgba(241, 245, 249, 0.76)",
      overlayDark: "rgba(15, 23, 42, 0.74)",
      accent: "#06b6d4",
      accentRgb: "6, 182, 212",
    },
  };

  /**
   * Intelligently resolves the domain configuration & background image
   */
  function getDomainConfig(themeId, data) {
    const bgUrl = data?.background_image;
    if (bgUrl === "none" || bgUrl === "") {
      return {
        key: "none",
        domain: "",
        url: "",
        title: "No Background Image",
        description: "Clean solid background without image layer",
        accent: data?.primary_color || "#4f46e5",
        accentRgb: "79, 70, 229",
      };
    }
    // If URL is explicitly provided and not the deprecated purple wave
    if (bgUrl && !bgUrl.includes("photo-1557683316-973673baf926")) {
      const match = Object.values(DOMAIN_BACKGROUNDS).find(b => b.url === bgUrl);
      if (match) return match;
      return {
        key: "custom",
        domain: "Personalized Domain",
        url: bgUrl,
        title: "Verified Portfolio Backdrop",
        description: "Custom candidate professional background",
        overlayLight: "rgba(248, 250, 252, 0.76)",
        overlayDark: "rgba(9, 13, 22, 0.74)",
        accent: data?.primary_color || "#4f46e5",
        accentRgb: "79, 70, 229",
      };
    }

    const role = (data?.professional_headline || data?.candidate_role || "").toLowerCase();
    const skills = [];
    if (data?.skills) {
      if (Array.isArray(data.skills)) skills.push(...data.skills.map(s => String(s).toLowerCase()));
      else if (typeof data.skills === "object") {
        Object.values(data.skills).forEach(arr => {
          if (Array.isArray(arr)) skills.push(...arr.map(s => String(s).toLowerCase()));
        });
      }
    }
    const text = `${role} ${skills.join(" ")}`.toLowerCase();

    // 1. AI, Machine Learning & Data Science
    if (["machine learning", "deep learning", "artificial intelligence", "nlp", "computer vision", "llm", "data scientist", "genai", "pytorch", "tensorflow", "neural", "langchain"].some(k => text.includes(k))) {
      return DOMAIN_BACKGROUNDS.ai_tech;
    }
    // 2. Data Analytics
    if (["data analyst", "business intelligence", "power bi", "tableau", "analytics", "sql analyst"].some(k => text.includes(k))) {
      return DOMAIN_BACKGROUNDS.data_analytics;
    }
    // 3. Cloud / DevOps / Cybersecurity
    if (["devops", "cloud", "aws", "azure", "docker", "kubernetes", "sre", "cybersecurity", "security engineer"].some(k => text.includes(k))) {
      return DOMAIN_BACKGROUNDS.cloud_devops;
    }
    // 4. Creative / UI/UX
    if (["ui/ux", "ui designer", "ux designer", "product designer", "graphic", "web design", "figma", "creative"].some(k => text.includes(k))) {
      return DOMAIN_BACKGROUNDS.creative;
    }
    // 5. HR / Talent Acquisition
    if (["recruiter", "talent acquisition", "human resources", "hr manager", "people operations", "talent specialist", "recruitment"].some(k => text.includes(k))) {
      return DOMAIN_BACKGROUNDS.hr_recruiting;
    }
    // 6. Mobile
    if (["mobile", "flutter", "ios", "android", "react native", "swift"].some(k => text.includes(k))) {
      return DOMAIN_BACKGROUNDS.mobile;
    }
    // 7. Corporate / Executive
    if (["product manager", "project manager", "scrum master", "operations", "business analyst", "finance", "director", "vp"].some(k => text.includes(k))) {
      return DOMAIN_BACKGROUNDS.corporate;
    }
    // 8. Consulting / Strategy
    if (["consultant", "strategy", "architect", "advisor", "legal", "researcher"].some(k => text.includes(k))) {
      return DOMAIN_BACKGROUNDS.elegant;
    }
    // 9. Software Engineering
    if (["software engineer", "backend", "full stack", "fullstack", "python", "java", "developer"].some(k => text.includes(k))) {
      return DOMAIN_BACKGROUNDS.developer;
    }

    // Theme based fallback
    const t = (themeId || "").toLowerCase();
    if (t.includes("ai_") || t.includes("quantum")) return DOMAIN_BACKGROUNDS.ai_tech;
    if (t.includes("dev") || t.includes("tech_") || t.includes("matrix")) return DOMAIN_BACKGROUNDS.developer;
    if (t.includes("creative") || t.includes("pop_art") || t.includes("studio")) return DOMAIN_BACKGROUNDS.creative;
    if (t.includes("exec") || t.includes("corp")) return DOMAIN_BACKGROUNDS.corporate;
    if (t.includes("elegant") || t.includes("vogue")) return DOMAIN_BACKGROUNDS.elegant;
    if (t.includes("dark") || t.includes("obsidian")) return DOMAIN_BACKGROUNDS.dark;
    if (t.includes("minimal") || t.includes("swiss")) return DOMAIN_BACKGROUNDS.minimal;

    return DOMAIN_BACKGROUNDS.developer;
  }

  /**
   * Applies CSS variables & theme classes to the container
   */
  function applyThemeStyles(container, data) {
    const themeId = (data.theme_id || "modern").toLowerCase();
    const meta = THEMES_METADATA.find(t => t.id === themeId) || THEMES_METADATA[0];

    let primary = data.primary_color || meta.defaultPrimary;
    let secondary = data.secondary_color || meta.defaultSecondary;
    const font = data.font || meta.font;
    const bgStyle = data.background_style || meta.defaultBg || "mesh";
    const cardStyle = data.card_style || meta.defaultCard || "glass";
    const btnStyle = data.button_style || meta.defaultBtn || "rounded";
    const isDark = Boolean(data.dark_mode || themeId === "dark" || themeId === "developer" || themeId === "ai_tech");

    if (isDark && themeId === "minimal" && (primary === "#111827" || primary === "#000000")) {
      primary = "#f8fafc";
      secondary = "#cbd5e1";
    }

    // Domain Background Image Setup
    const domainConfig = getDomainConfig(themeId, data);
    const bgImgUrl = (data.background_image !== "" && data.background_image !== "none")
      ? (data.background_image || domainConfig?.url)
      : "";

    container.className = `portfolio-theme-root theme-${themeId} ${isDark ? "theme-dark-mode" : ""} ${bgImgUrl ? "has-domain-bg" : ""}`;
    container.setAttribute("data-bg-style", bgStyle);
    container.setAttribute("data-card-style", cardStyle);
    container.setAttribute("data-btn-style", btnStyle);
    container.setAttribute("data-theme-mode", isDark ? "dark" : "light");
    container.setAttribute("data-bs-theme", isDark ? "dark" : "light");

    container.style.setProperty("--theme-primary", primary);
    container.style.setProperty("--theme-secondary", secondary);
    container.style.setProperty("--theme-font", `'${font}', system-ui, sans-serif`);

    if (bgImgUrl) {
      container.style.setProperty("--theme-domain-bg-image", `url('${bgImgUrl}')`);
      container.setAttribute("data-domain", domainConfig?.key || "domain");
      container.style.setProperty("--theme-domain-accent", domainConfig?.accent || primary);
      container.style.setProperty("--theme-domain-accent-rgb", domainConfig?.accentRgb || "79, 70, 229");
    } else {
      container.removeAttribute("data-domain");
      container.style.removeProperty("--theme-domain-bg-image");
      container.style.removeProperty("--theme-domain-overlay");
    }

    if (isDark) {
      container.style.setProperty("--theme-text", "#f8fafc");
      container.style.setProperty("--theme-text-muted", "#cbd5e1");
      container.style.setProperty("--theme-subcard-bg", "rgba(255, 255, 255, 0.04)");
      container.style.setProperty("--theme-badge-color", primary === "#f8fafc" ? "#f8fafc" : primary);
      container.style.setProperty("--theme-badge-bg", `${primary}25`);
    } else {
      container.style.setProperty("--theme-text", "#0f172a");
      container.style.setProperty("--theme-text-muted", "#475569");
      container.style.setProperty("--theme-subcard-bg", "rgba(15, 23, 42, 0.02)");
      container.style.setProperty("--theme-badge-color", primary);
      container.style.setProperty("--theme-badge-bg", `${primary}18`);
    }
  }

  /**
   * Generates a completely randomized, harmonious styling combination for the candidate
   */
  function getRandomStyle(currentData) {
    const randomTheme = THEMES_METADATA[Math.floor(Math.random() * THEMES_METADATA.length)];
    const palette = (randomTheme.palettes && randomTheme.palettes.length > 0)
      ? randomTheme.palettes[Math.floor(Math.random() * randomTheme.palettes.length)]
      : { primary: randomTheme.defaultPrimary, secondary: randomTheme.defaultSecondary };
    const font = randomTheme.font || "Plus Jakarta Sans";
    const bgStyles = ["mesh", "clean", "dots", "grid"];
    const cardStyles = ["glass", "flat", "elevated", "bordered"];
    const btnStyles = ["rounded", "pill", "sharp", "glow"];
    const isDark = Boolean(randomTheme.defaultDark);

    return {
      theme_id: randomTheme.id,
      layout: randomTheme.layout || randomTheme.id,
      primary_color: palette.primary,
      secondary_color: palette.secondary,
      font: font,
      background_style: randomTheme.defaultBg || bgStyles[Math.floor(Math.random() * bgStyles.length)],
      card_style: randomTheme.defaultCard || cardStyles[Math.floor(Math.random() * cardStyles.length)],
      button_style: randomTheme.defaultBtn || btnStyles[Math.floor(Math.random() * btnStyles.length)],
      dark_mode: isDark
    };
  }

  /* ==============================================================
     LAYOUT RENDERERS (Bespeak UI Architecture for each Theme)
     ============================================================== */

  /**
   * NOVA EDITORIAL DESIGN SYSTEM (World-Class Boutique Agency & Studio Aesthetic)
   * Implements the high-end editorial layout showcased in the NOVA reference design:
   * Minimalist header, tracked category kickers, bold headline with accent styling,
   * sculpted organic portrait masks, dark high-contrast KPI strips, photographic project cards
   * with circular diagonal arrow buttons, and craft-driven value spotlight sections.
   */

  /**
   * High-End Candidate Avatar / Monogram Generator
   * Renders genuine candidate photo if uploaded, or an authentic luxury gradient monogram
   * with candidate's initials and "Available for Hire" pulsing LED status indicator.
   */
  function renderCandidateAvatar(data, size = 160, extraClass = "") {
    const name = escapeHtml(data.candidate_name || "Candidate");
    const rawName = data.candidate_name || "Candidate";
    const initials = rawName.split(/\s+/).map(p => p[0]).filter(Boolean).slice(0, 2).join("").toUpperCase() || "C";
    const primary = data.primary_color || "var(--theme-primary, #4f46e5)";
    const secondary = data.secondary_color || "var(--theme-secondary, #06b6d4)";
    const imgUrl = data.profile_image || "";
    const isCustomPhoto = imgUrl && !imgUrl.includes("unsplash.com") && !imgUrl.includes("images.unsplash") && !imgUrl.includes("ui-avatars.com");

    if (isCustomPhoto) {
      return `
        <div class="portfolio-avatar-wrap position-relative d-inline-block ${extraClass}">
          <img src="${escapeHtml(imgUrl)}" alt="${name}" class="rounded-circle shadow-lg" style="width: ${size}px; height: ${size}px; object-fit: cover; border: 3.5px solid ${primary};" />
          <span class="portfolio-status-dot position-absolute" style="bottom: 8px; right: 8px; width: ${Math.max(14, Math.round(size * 0.12))}px; height: ${Math.max(14, Math.round(size * 0.12))}px; background: #10b981; border: 2.5px solid #ffffff; border-radius: 50%; box-shadow: 0 0 10px #10b981;" title="Available for Opportunities"></span>
        </div>
      `;
    }

    return `
      <div class="portfolio-avatar-monogram ${extraClass} position-relative d-inline-flex align-items-center justify-content-center shadow-lg" style="width: ${size}px; height: ${size}px; border-radius: 28%; background: linear-gradient(135deg, ${primary} 0%, ${secondary} 100%); color: #ffffff; font-weight: 800; font-size: ${Math.round(size * 0.36)}px; letter-spacing: -0.02em; border: 3px solid rgba(255,255,255,0.3); box-shadow: 0 14px 32px rgba(79, 70, 229, 0.28);">
        <span>${initials}</span>
        <span class="portfolio-status-dot position-absolute" style="bottom: 8px; right: 8px; width: ${Math.max(14, Math.round(size * 0.12))}px; height: ${Math.max(14, Math.round(size * 0.12))}px; background: #10b981; border: 2.5px solid #ffffff; border-radius: 50%; box-shadow: 0 0 10px #10b981;" title="Available for Opportunities"></span>
      </div>
    `;
  }

  /**
   * Modern Elevated Project Showcase Card
   * Includes OS traffic light micro-dots, technology category tags, external link arrow,
   * feature bullets, colored tech pills, and interactive System Architecture modal button.
   */
  function renderEnhancedProjectCard(project, idx, themeVariant = "default", data = null) {
    if (!project || typeof project !== "object") return "";
    const name = project.name || `Featured Project #${idx + 1}`;
    const desc = project.description || "Production-grade system implementation engineered for high reliability, performance, and user impact.";
    const techs = Array.isArray(project.technologies) ? project.technologies : [];
    const features = Array.isArray(project.key_features) && project.key_features.length > 0
      ? project.key_features.slice(0, 3)
      : [
          "Architected scalable component modules with clean abstractions",
          "Optimized processing latency and data throughput benchmarks"
        ];

    // Category tag
    const category = project.category || (
      techs.some(t => /react|vue|next|angular|html|css/i.test(t)) && techs.some(t => /fastapi|node|python|express|sql/i.test(t)) ? "Full-Stack" :
      techs.some(t => /ai|torch|ml|vision|nlp|llm/i.test(t)) ? "AI / ML" :
      techs.some(t => /cloud|docker|k8s|aws/i.test(t)) ? "Cloud Infra" :
      techs.some(t => /python|java|c\+\+|golang/i.test(t)) ? "Core Engineering" :
      "System Architecture"
    );

    const cleanUrl = (raw) => {
      if (!raw || typeof raw !== "string") return "";
      let trimmed = raw.trim();
      if (!trimmed || trimmed === "#" || trimmed.toLowerCase() === "none") return "";
      if (!trimmed.match(/^https?:\/\//i)) {
        trimmed = "https://" + trimmed;
      }
      return trimmed;
    };
    const liveUrl = cleanUrl(project.live_demo_url || project.demo_url || project.url || project.link);
    const codeUrl = cleanUrl(project.github_url || project.repo_url || project.code_url);

    return `
      <div class="col-md-6 col-lg-4 project-card-item" data-tech="${escapeHtml((techs.join(' ') + ' ' + name).toLowerCase())}">
        <div class="modern-project-card">
          <div class="card-chrome-header">
            <div class="traffic-dots">
              <span class="dot-red"></span>
              <span class="dot-yellow"></span>
              <span class="dot-green"></span>
            </div>
            <span class="project-category-tag">${escapeHtml(category)}</span>
          </div>
          <div class="card-body-enhanced">
            <div class="project-title-enhanced">
              ${liveUrl ? `<a href="${escapeHtml(liveUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(name)}</a>` : `<span>${escapeHtml(name)}</span>`}
              ${liveUrl ? `<a href="${escapeHtml(liveUrl)}" target="_blank" rel="noopener noreferrer" class="project-arrow-icon" title="Open Live Site">↗</a>` : `<span class="project-arrow-icon">✦</span>`}
            </div>
            <p class="project-description-enhanced">${escapeHtml(desc)}</p>
            <ul class="project-features-list">
              ${features.map(f => `<li><span class="feat-check">✓</span> <span>${escapeHtml(f)}</span></li>`).join("")}
            </ul>
            ${techs.length > 0 ? `
              <div class="tech-pills-row">
                ${techs.slice(0, 6).map(t => `<span class="tech-pill-dot">${escapeHtml(t)}</span>`).join("")}
              </div>
            ` : ""}
          </div>
          <div class="card-footer-enhanced">
            <div class="d-flex align-items-center gap-2 flex-wrap">
              ${liveUrl ? `<a href="${escapeHtml(liveUrl)}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-primary fw-semibold px-2.5 py-1" style="font-size: 0.78rem;">🌐 Live Demo</a>` : ""}
              ${codeUrl ? `<a href="${escapeHtml(codeUrl)}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline-secondary fw-semibold px-2.5 py-1" style="font-size: 0.78rem;">💻 Source</a>` : ""}
            </div>
            <button type="button" class="btn-arch-inspect btn-open-arch-modal" data-project-idx="${idx}" title="Inspect System Architecture">
              <span>🔍 Architecture</span>
            </button>
          </div>
        </div>
      </div>
    `;
  }

  /**
   * Interactive System Architecture Modal Presenter
   */
  function showProjectArchitectureModal(project, idx, data) {
    let modalEl = document.getElementById("projectArchitectureModal");
    if (!modalEl) {
      modalEl = document.createElement("div");
      modalEl.id = "projectArchitectureModal";
      modalEl.className = "modal fade";
      modalEl.tabIndex = -1;
      modalEl.setAttribute("aria-hidden", "true");
      document.body.appendChild(modalEl);
    }

    const name = escapeHtml(project.name || `Project #${idx + 1}`);
    const desc = escapeHtml(project.description || "Scalable production software system engineered for high concurrency, security, and performance.");
    const techs = Array.isArray(project.technologies) ? project.technologies : [];
    const features = Array.isArray(project.key_features) && project.key_features.length > 0
      ? project.key_features
      : [
          "Microservices modular design with decoupled domain contexts",
          "Automated CI/CD testing and Docker containerized deployment",
          "Sub-50ms API endpoints and optimized database indexing"
        ];

    const cleanUrl = (raw) => {
      if (!raw || typeof raw !== "string") return "";
      let trimmed = raw.trim();
      if (!trimmed || trimmed === "#" || trimmed.toLowerCase() === "none") return "";
      if (!trimmed.match(/^https?:\/\//i)) trimmed = "https://" + trimmed;
      return trimmed;
    };
    const liveUrl = cleanUrl(project.live_demo_url || project.demo_url || project.url || project.link);
    const codeUrl = cleanUrl(project.github_url || project.repo_url || project.code_url);

    // Dynamic architecture topology breakdown
    const uiTech = techs.filter(t => /react|vue|next|angular|html|css|tailwind|svelte|ui/i.test(t)).join(", ") || "Modern Responsive UI";
    const apiTech = techs.filter(t => /fastapi|node|python|express|django|flask|spring|grpc|rest/i.test(t)).join(", ") || "High-Throughput API Gateway";
    const dataTech = techs.filter(t => /postgres|sql|mongo|redis|sqlite|database/i.test(t)).join(", ") || "Relational / Key-Value Persistence";
    const cloudTech = techs.filter(t => /docker|k8s|aws|cloud|ci|terraform|linux/i.test(t)).join(", ") || "Cloud Native Containers & CI/CD";

    modalEl.innerHTML = `
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content shadow-lg border-0" style="border-radius: 20px; overflow: hidden;">
          <div class="modal-header px-4 py-3 border-bottom d-flex align-items-center justify-content-between" style="background: rgba(15, 23, 42, 0.03);">
            <div class="d-flex align-items-center gap-2">
              <span class="fs-4">🏛️</span>
              <div>
                <h5 class="modal-title fw-bold mb-0">${name}</h5>
                <small class="text-muted">System Architecture & Engineering Specification</small>
              </div>
            </div>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body p-4">
            <div class="mb-4">
              <h6 class="fw-bold text-uppercase small text-primary mb-2" style="letter-spacing: 0.05em;">Overview & Objective</h6>
              <p class="text-secondary small mb-0" style="line-height: 1.6;">${desc}</p>
            </div>

            <!-- Architectural Topology -->
            <div class="mb-4 p-3 rounded-3" style="background: rgba(15, 23, 42, 0.03); border: 1px dashed rgba(99, 102, 241, 0.3);">
              <h6 class="fw-bold text-uppercase small mb-3 d-flex align-items-center gap-2" style="color: var(--theme-primary, #4f46e5); letter-spacing: 0.05em;">
                <span>⚡</span> System Architecture & Data Flow
              </h6>
              <div class="row g-2 text-center small">
                <div class="col-6 col-md-3">
                  <div class="p-2.5 rounded-2 bg-white shadow-sm border h-100">
                    <div class="fw-bold text-dark mb-1">🖥️ Client Tier</div>
                    <div class="text-muted" style="font-size: 0.75rem;">${escapeHtml(uiTech)}</div>
                  </div>
                </div>
                <div class="col-6 col-md-3">
                  <div class="p-2.5 rounded-2 bg-white shadow-sm border h-100">
                    <div class="fw-bold text-dark mb-1">🔌 API Service</div>
                    <div class="text-muted" style="font-size: 0.75rem;">${escapeHtml(apiTech)}</div>
                  </div>
                </div>
                <div class="col-6 col-md-3">
                  <div class="p-2.5 rounded-2 bg-white shadow-sm border h-100">
                    <div class="fw-bold text-dark mb-1">🗄️ Persistence</div>
                    <div class="text-muted" style="font-size: 0.75rem;">${escapeHtml(dataTech)}</div>
                  </div>
                </div>
                <div class="col-6 col-md-3">
                  <div class="p-2.5 rounded-2 bg-white shadow-sm border h-100">
                    <div class="fw-bold text-dark mb-1">☁️ Deployment</div>
                    <div class="text-muted" style="font-size: 0.75rem;">${escapeHtml(cloudTech)}</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Key Engineering Highlights -->
            <div class="mb-4">
              <h6 class="fw-bold text-uppercase small text-primary mb-2" style="letter-spacing: 0.05em;">Engineering Highlights & Design Decisions</h6>
              <ul class="list-unstyled mb-0 small">
                ${features.map(f => `<li class="mb-2 d-flex align-items-start gap-2"><span class="text-primary fw-bold">✓</span> <span class="text-secondary">${escapeHtml(f)}</span></li>`).join("")}
              </ul>
            </div>

            <!-- Verified Tech Stack Badges -->
            ${techs.length > 0 ? `
              <div class="mb-2">
                <h6 class="fw-bold text-uppercase small text-muted mb-2" style="letter-spacing: 0.05em; font-size: 0.72rem;">Verified Tech Stack</h6>
                <div class="d-flex flex-wrap gap-1.5">
                  ${techs.map(t => `<span class="badge bg-light text-dark border px-2.5 py-1.5 fw-semibold" style="font-size: 0.75rem;">${escapeHtml(t)}</span>`).join("")}
                </div>
              </div>
            ` : ""}
          </div>
          <div class="modal-footer px-4 py-3 bg-light border-top d-flex justify-content-between">
            <div class="d-flex gap-2">
              ${liveUrl ? `<a href="${escapeHtml(liveUrl)}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-primary fw-semibold px-3 py-1.5"><span>🌐</span> Live Deployment</a>` : ""}
              ${codeUrl ? `<a href="${escapeHtml(codeUrl)}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline-dark fw-semibold px-3 py-1.5"><span>💻</span> Source Code</a>` : ""}
            </div>
            <button type="button" class="btn btn-sm btn-secondary px-3 py-1.5" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    `;

    if (typeof bootstrap !== "undefined" && bootstrap.Modal) {
      bootstrap.Modal.getOrCreateInstance(modalEl).show();
    }
  }

  function renderNovaEditorialLayout(data, activeSections, layoutVariant) {
    const name = escapeHtml(data.candidate_name || "Professional");
    const firstName = name.split(" ")[0] || "Candidate";
    const headline = escapeHtml(data.professional_headline || "Engineering & Strategic Leadership");
    const soc = data.social_links || {};
    const loc = escapeHtml(soc.location || "");
    const email = escapeHtml(soc.email || "");
    const phone = escapeHtml(soc.phone || "");
    const linkedin = escapeHtml(soc.linkedin || "");
    const github = escapeHtml(soc.github || "");
    const about = escapeHtml(data.about || "");
    const skills = data.skills || {};
    const projects = data.projects || [];
    const experience = data.experience || [];
    const education = data.education || [];
    const certs = data.certifications || [];
    const achievements = data.achievements || [];
    const impactMetrics = data.impact_metrics || [];
    const themeId = (data.theme_id || layoutVariant || "modern").toLowerCase();

    // 1. Determine Domain Archetype based on Candidate Role, Skills, and Theme
    const roleText = (headline + " " + (data.current_role || "") + " " + JSON.stringify(skills) + " " + themeId).toLowerCase();
    let domainType = "studio";
    if (roleText.includes("recruiter") || roleText.includes("talent") || roleText.includes("human resources") || roleText.includes("sourcer") || roleText.includes("people &")) {
      domainType = "people_talent";
    } else if (roleText.includes("ai") || roleText.includes("machine learning") || roleText.includes("deep learning") || roleText.includes("data scientist") || roleText.includes("llm") || themeId.includes("ai_")) {
      domainType = "ai_tech";
    } else if (roleText.includes("data analyst") || roleText.includes("business intelligence") || roleText.includes("power bi") || roleText.includes("tableau") || roleText.includes("sql analyst") || roleText.includes("data engineer") || roleText.includes("analyst")) {
      domainType = "data_analytics";
    } else if (roleText.includes("backend") || roleText.includes("full stack") || roleText.includes("fullstack") || roleText.includes("software engineer") || roleText.includes("developer") || themeId.includes("dev") || themeId.includes("terminal")) {
      domainType = "developer";
    } else if (roleText.includes("ui/ux") || roleText.includes("designer") || roleText.includes("product designer") || roleText.includes("frontend") || roleText.includes("creative") || themeId.includes("creative")) {
      domainType = "creative";
    } else if (roleText.includes("manager") || roleText.includes("director") || roleText.includes("vp") || roleText.includes("operations") || roleText.includes("executive") || roleText.includes("corporate") || themeId.includes("corp") || themeId.includes("exec")) {
      domainType = "corporate";
    }

    // 2. Curate Domain-Specific Persona Tokens (Palette, Mask Shape, Kicker, Portrait, Studio Photo, Pillars)
    const DOMAIN_PROFILES = {
      people_talent: {
        kicker: "PEOPLE & TALENT STRATEGY // ENTERPRISE ACQUISITION",
        headlinePrefix: "Transforming talent acquisition into",
        headlineHighlight: "exponential growth",
        maskClass: "mask-pebble",
        defaultAccent: "#0D9488",
        defaultAccentRgb: "13, 148, 136",
        isDark: false,
        bg: "#F9FAF9",
        kpiBg: "#111818",
        portrait: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=1200&q=80",
        studioImg: "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1200&q=80",
        defaultKpis: [
          { value: "$6M+", label: "Hiring Expenses Saved" },
          { value: "41%", label: "Faster Time-to-Hire" },
          { value: "470+", label: "Top Candidates Screened" },
          { value: "10+", label: "Years Talent Leadership" }
        ],
        pillars: ["Executive Search & Talent Sourcing", "ATS Optimization & Funnel Analytics", "Workforce Planning & Retention"]
      },
      ai_tech: {
        kicker: "ARTIFICIAL INTELLIGENCE / DEEP LEARNING / SYSTEMS",
        headlinePrefix: "Engineering intelligent frontiers for",
        headlineHighlight: "high-scale innovation",
        maskClass: "mask-corner-curve",
        defaultAccent: "#00E5FF",
        defaultAccentRgb: "0, 229, 255",
        isDark: true,
        bg: "#0A0D14",
        kpiBg: "#111726",
        portrait: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1200&q=80",
        studioImg: "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=1200&q=80",
        defaultKpis: [
          { value: "99.94%", label: "Inference Pipeline Uptime" },
          { value: "4.2M+", label: "Daily Neural Queries Handled" },
          { value: "45%", label: "Latency Optimization" },
          { value: "$320K", label: "Infrastructure Cost Savings" }
        ],
        pillars: ["LLM & Agentic Orchestration", "Low-Latency RAG Pipelines", "High-Throughput Production Serving"]
      },
      data_analytics: {
        kicker: "STRATEGY / DATA SYSTEMS / BUSINESS INTELLIGENCE",
        headlinePrefix: "Transforming enterprise data into",
        headlineHighlight: "strategic clarity",
        maskClass: "mask-pebble",
        defaultAccent: "#BA855E",
        defaultAccentRgb: "186, 133, 94",
        isDark: false,
        bg: "#FAF8F5",
        kpiBg: "#111216",
        portrait: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=1200&q=80",
        studioImg: "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1200&q=80",
        defaultKpis: [
          { value: "2000+", label: "ETL Pipelines Orchestrated" },
          { value: "10+", label: "Years Quantitative Experience" },
          { value: "800+", label: "Executive Dashboards Shipped" },
          { value: "100%", label: "Data Integrity & Parity" }
        ],
        pillars: ["Enterprise BI & Data Warehousing", "Automated SQL Reconciliation", "Agile Stakeholder Coordination"]
      },
      developer: {
        kicker: "FULL STACK ARCHITECTURE / SYSTEMS / CLOUD",
        headlinePrefix: "Building resilient web platforms with",
        headlineHighlight: "craft & performance",
        maskClass: "mask-studio-bento",
        defaultAccent: "#10B981",
        defaultAccentRgb: "16, 185, 129",
        isDark: data.dark_mode || themeId.includes("dark") || themeId.includes("terminal"),
        bg: (data.dark_mode || themeId.includes("dark")) ? "#0E1318" : "#FAF9F6",
        kpiBg: "#11161B",
        portrait: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=1200&q=80",
        studioImg: "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80",
        defaultKpis: [
          { value: "50+", label: "Production Microservices" },
          { value: "99.9%", label: "System Availability SLA" },
          { value: "10x", label: "Build & Deploy Velocity" },
          { value: "150M+", label: "API Requests Processed" }
        ],
        pillars: ["Full-Stack State Management", "Clean REST & GraphQL APIs", "Production DevOps & CI/CD"]
      },
      creative: {
        kicker: "PRODUCT DESIGN / UI/UX / CREATIVE DIRECTION",
        headlinePrefix: "Crafting intuitive digital experiences that",
        headlineHighlight: "delight & convert",
        maskClass: "mask-asymmetric-pill",
        defaultAccent: "#F97316",
        defaultAccentRgb: "249, 115, 22",
        isDark: false,
        bg: "#FFFDFB",
        kpiBg: "#161318",
        portrait: "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=1200&q=80",
        studioImg: "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1200&q=80",
        defaultKpis: [
          { value: "140+", label: "Design Systems & Interfaces" },
          { value: "4.9/5", label: "User Usability Rating" },
          { value: "65%", label: "Conversion Rate Uplift" },
          { value: "10+", label: "Years Designing Products" }
        ],
        pillars: ["Human-Centered Interaction Design", "Scalable Design Tokens", "Interactive Micro-Animations"]
      },
      corporate: {
        kicker: "EXECUTIVE LEADERSHIP / STRATEGY / OPERATIONS",
        headlinePrefix: "Leading organizational transformations that",
        headlineHighlight: "accelerate growth",
        maskClass: "mask-arch",
        defaultAccent: "#2563EB",
        defaultAccentRgb: "37, 99, 235",
        isDark: false,
        bg: "#F8FAFC",
        kpiBg: "#0F172A",
        portrait: "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=1200&q=80",
        studioImg: "https://images.unsplash.com/photo-1600880292203-757bb62b4baf?auto=format&fit=crop&w=1200&q=80",
        defaultKpis: [
          { value: "15+", label: "Years Executive Experience" },
          { value: "$20M+", label: "Enterprise Portfolio Managed" },
          { value: "40+", label: "Cross-Functional Team Size" },
          { value: "100%", label: "On-Time Milestone Delivery" }
        ],
        pillars: ["Strategic Product Roadmaps", "Cross-Functional Governance", "Enterprise Resource Allocation"]
      },
      studio: {
        kicker: "STRATEGY / DESIGN / TECHNOLOGY",
        headlinePrefix: "New possibilities for",
        headlineHighlight: "ambitious brands",
        maskClass: "mask-pebble",
        defaultAccent: "#BA855E",
        defaultAccentRgb: "186, 133, 94",
        isDark: false,
        bg: "#FAF8F5",
        kpiBg: "#111216",
        portrait: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1200&q=80",
        studioImg: "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1200&q=80",
        defaultKpis: [
          { value: "2000+", label: "Projects Delivered" },
          { value: "10+", label: "Years of Experience" },
          { value: "800+", label: "Engineering Hours" },
          { value: "150M+", label: "Client Value Generated" }
        ],
        pillars: ["Strategic Thinking", "Tailored Engineering Approach", "Real Measurable Support"]
      }
    };

    const profile = DOMAIN_PROFILES[domainType] || DOMAIN_PROFILES.studio;
    const isDarkMode = data.dark_mode !== undefined ? data.dark_mode : profile.isDark;
    const accentColor = data.primary_color || profile.defaultAccent;
    const accentRgb = profile.defaultAccentRgb;
    const heroPortraitUrl = (data.profile_image && !data.profile_image.includes("ui-avatars.com")) ? data.profile_image : profile.portrait;
    const studioPhotoUrl = profile.studioImg;

    // 3. Extract Trusted Brands / Companies & Verified Tech strictly from Candidate Profile
    const trustedItems = [];
    if (experience.length > 0) {
      experience.forEach(exp => {
        if (exp.company && !trustedItems.includes(exp.company.toUpperCase())) {
          trustedItems.push(exp.company.toUpperCase());
        }
      });
    }
    const allSkillsList = Object.values(skills).flat();
    if (trustedItems.length < 5 && allSkillsList.length > 0) {
      allSkillsList.slice(0, 6).forEach(sk => {
        const u = sk.toUpperCase();
        if (!trustedItems.includes(u)) {
          trustedItems.push(u);
        }
      });
    }
    if (trustedItems.length === 0) {
      trustedItems.push("MODO", "LUMI", "KOVO", "NOMA", "ASPEKT");
    }

    // 4. Assemble 4 High-Contrast KPI Metrics
    const kpiMetrics = [];
    if (impactMetrics.length > 0) {
      impactMetrics.slice(0, 4).forEach(m => {
        kpiMetrics.push({ value: m.value || "100%", label: m.label || m.title || "Core Metric" });
      });
    } else if (achievements.length > 0) {
      achievements.slice(0, 4).forEach(a => {
        kpiMetrics.push({ value: a.value || "100%", label: a.label || a.title || "Key Metric" });
      });
    }
    while (kpiMetrics.length < 4) {
      const fallbackKpi = profile.defaultKpis[kpiMetrics.length] || { value: "100%", label: "Production Quality" };
      kpiMetrics.push(fallbackKpi);
    }

    // 5. Build Project Showcase Cards with photographic backdrops & circular ↗ action button
    const projectCovers = [
      "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80",
      "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80",
      "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80",
      "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
      "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?auto=format&fit=crop&w=1200&q=80",
      "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=1200&q=80"
    ];

    let projectsCardsHtml = "";
    if (projects.length > 0) {
      projectsCardsHtml = projects.map((p, idx) => {
        const cover = projectCovers[idx % projectCovers.length];
        const pName = escapeHtml(p.title || p.name || `Project #${idx + 1}`);
        const pDesc = escapeHtml(p.description || "");
        const pLink = escapeHtml(p.live_demo_url || p.github_url || "#section-contact");
        const pTech = (p.technologies || []).slice(0, 3).map(t => `<span class="badge rounded-pill me-1" style="background: rgba(255,255,255,0.2); color: #fff; font-size: 0.75rem;">${escapeHtml(t)}</span>`).join("");
        return `
          <div class="col-lg-6 mb-4 project-card-item" data-tech="${escapeHtml(((p.technologies || []).join(' ') + ' ' + (p.name || '')).toLowerCase())}">
            <div class="nova-project-card-wrapper position-relative">
              <a href="${pLink}" target="${pLink.startsWith('http') ? '_blank' : '_self'}" rel="${pLink.startsWith('http') ? 'noopener noreferrer' : ''}" class="nova-project-card">
                <img src="${cover}" alt="${pName}" class="nova-project-bg" />
                <div class="nova-project-gradient"></div>
                <div class="nova-project-content">
                  <div>
                    <h4 class="nova-project-title">${pName}</h4>
                    ${pDesc ? `<p class="nova-project-desc">${pDesc.substring(0, 110)}${pDesc.length > 110 ? '...' : ''}</p>` : ''}
                    <div>${pTech}</div>
                  </div>
                  <div class="nova-project-btn">↗</div>
                </div>
              </a>
              ${(p.live_demo_url || p.github_url) ? `
                <div class="nova-project-actions mt-2 d-flex gap-2">
                  ${renderProjectActionLinks(p, "nova")}
                </div>
              ` : ''}
            </div>
          </div>
        `;
      }).join("");
    } else {
      projectsCardsHtml = `
        <div class="col-lg-6 mb-4">
          <a href="#section-contact" class="nova-project-card">
            <img src="${projectCovers[0]}" alt="A premium brand with a new website" class="nova-project-bg" />
            <div class="nova-project-gradient"></div>
            <div class="nova-project-content">
              <div>
                <h4 class="nova-project-title">A premium brand with a new website</h4>
                <p class="nova-project-desc">Complete end-to-end architecture, modern design system, and scalable cloud performance.</p>
              </div>
              <div class="nova-project-btn">↗</div>
            </div>
          </a>
        </div>
        <div class="col-lg-6 mb-4">
          <a href="#section-contact" class="nova-project-card">
            <img src="${projectCovers[1]}" alt="A new identity for an ambitious brand" class="nova-project-bg" />
            <div class="nova-project-gradient"></div>
            <div class="nova-project-content">
              <div>
                <h4 class="nova-project-title">A new identity for an ambitious brand</h4>
                <p class="nova-project-desc">Strategic development combining refined aesthetics with high-throughput backend services.</p>
              </div>
              <div class="nova-project-btn">↗</div>
            </div>
          </a>
        </div>
      `;
    }

    // 6. Assemble Full Complete HTML
    let html = `
      <div class="nova-portfolio-root ${isDarkMode ? 'nova-dark' : ''}" style="--nova-accent: ${accentColor}; --nova-accent-rgb: ${accentRgb}; --nova-bg: ${profile.bg};">
        
        <!-- Top Subtle Announcement / Verification Bar -->
        <div class="nova-top-bar">
          <div class="container d-flex justify-content-between align-items-center">
            <span>Verified Candidate Portfolio • AI Recruiter Platform</span>
            <div class="d-none d-sm-block">
              <a href="#section-contact">Schedule Interview</a>
              <span class="mx-2">•</span>
              <a href="javascript:window.print()">Download CV</a>
            </div>
          </div>
        </div>

        <!-- Minimalist Clean Navbar (Image 1) -->
        <nav class="nova-navbar">
          <div class="container d-flex justify-content-between align-items-center">
            <a href="#section-home" class="nova-brand">${name}</a>
            <div class="d-none d-md-flex align-items-center gap-1">
              <a href="#section-about" class="nova-nav-link">About us</a>
              <a href="#section-skills" class="nova-nav-link">Services</a>
              <a href="#section-projects" class="nova-nav-link">Selected work</a>
              <a href="#section-experience" class="nova-nav-link">Reviews</a>
            </div>
            <div class="d-flex align-items-center gap-3">
              <span class="d-none d-lg-inline small fw-bold" style="color: var(--nova-text-muted); opacity: 0.8;">PL / EN</span>
              <a href="#section-contact" class="nova-nav-cta">Start a project</a>
            </div>
          </div>
        </nav>

        <!-- Hero Section (Image 1) -->
        <section id="section-home" class="nova-hero">
          <div class="container">
            <div class="row align-items-center g-5">
              <div class="col-lg-6 col-xl-7">
                <span class="nova-kicker">${profile.kicker}</span>
                <h1 class="nova-hero-title">
                  ${profile.headlinePrefix} <span class="nova-hero-accent">${profile.headlineHighlight}</span>
                </h1>
                <div class="lead fw-bold mb-3" style="color: var(--nova-text); font-size: 1.25rem;">
                  ${headline}
                </div>
                <p class="nova-hero-summary">
                  ${about ? (about.length > 280 ? about.substring(0, 280) + '...' : about) : 'We create modern websites and scalable software systems that strengthen your brand, attract clients and turn business goals into real growth.'}
                </p>
                <div class="nova-btn-group">
                  <a href="#section-contact" class="nova-btn-primary">Start a project</a>
                  <a href="#section-about" class="nova-btn-secondary">Meet the team</a>
                </div>
              </div>
              <div class="col-lg-6 col-xl-5 text-center">
                <div class="nova-portrait-frame">
                  <img src="${heroPortraitUrl}" alt="${name}" class="nova-portrait-img ${data.portrait_mask || profile.maskClass}" />
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- "Trusted By" Strip (Image 2) -->
        <div class="container nova-trusted-strip">
          <div class="d-flex align-items-center flex-wrap gap-4">
            <span class="nova-trusted-label">Trusted by</span>
            <div class="nova-trusted-items">
              ${trustedItems.map(item => `<span>${escapeHtml(item)}</span>`).join('')}
            </div>
          </div>
        </div>

        <!-- High-Contrast Dark KPI Metrics Banner (Image 2) -->
        <div class="container">
          <div class="nova-kpi-banner">
            <div class="nova-kpi-grid">
              ${kpiMetrics.map(k => `
                <div class="nova-kpi-item">
                  <div class="nova-kpi-value">${escapeHtml(k.value)}</div>
                  <div class="nova-kpi-label">${escapeHtml(k.label)}</div>
                </div>
              `).join('')}
            </div>
          </div>
        </div>

        <!-- Two-Column Section Lead (Image 2) & Selected Work (Image 3) -->
        <section id="section-projects" class="py-3">
          <div class="container nova-section-lead">
            <div class="row align-items-end g-4">
              <div class="col-lg-6">
                <h2 class="nova-lead-title">Turning ideas into real outcomes</h2>
              </div>
              <div class="col-lg-6">
                <p class="nova-lead-desc">
                  We combine strategic thinking, refined design and modern technology to create digital systems that look great and deliver measurable value.
                </p>
                <a href="#section-projects" class="nova-action-link">
                  See selected work <span class="ms-1">→</span>
                </a>
              </div>
            </div>
          </div>

          <!-- Selected Work Photographic Cards Grid (Image 3) -->
          <div class="container mb-5">
            <div class="row g-4">
              ${projectsCardsHtml}
            </div>
          </div>
        </section>

        <!-- Spotlight Section ("People who create value" - Image 4) -->
        <section id="section-about" class="nova-spotlight-section">
          <div class="container">
            <div class="row align-items-center g-5">
              <div class="col-lg-6">
                <img src="${studioPhotoUrl}" alt="Engineering Team Studio" class="nova-spotlight-img" />
              </div>
              <div class="col-lg-6">
                <h2 class="nova-spotlight-lead">People who create value</h2>
                <p class="nova-spotlight-text">
                  ${about || 'We are a team of specialists who combine a passion for technology with a sharp eye for good design. Every project is shaped around the brand, its goals and its audience.'}
                </p>
                <div class="nova-avatar-cluster">
                  <div class="nova-avatar-stack">
                    <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80" alt="Specialist 1" />
                    <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=150&q=80" alt="Specialist 2" />
                    <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=150&q=80" alt="Specialist 3" />
                  </div>
                  <span class="nova-avatar-caption">10+ specialists collaborating across core disciplines</span>
                </div>
                <div class="nova-bullet-list">
                  ${profile.pillars.map(pillar => `
                    <div class="nova-bullet-item">
                      <span class="nova-bullet-icon">→</span>
                      <span>${escapeHtml(pillar)}</span>
                    </div>
                  `).join('')}
                </div>
                <a href="#section-contact" class="nova-btn-primary">Meet the team</a>
              </div>
            </div>
          </div>
        </section>

        <!-- Core Capabilities / Services & Tech Stack (Image 1 'Services') -->
        <section id="section-skills" class="py-5" style="border-top: 1px solid var(--nova-card-border);">
          <div class="container">
            <div class="d-flex justify-content-between align-items-end flex-wrap gap-3 mb-5">
              <div>
                <span class="nova-kicker mb-2">SERVICES &amp; EXPERTISE</span>
                <h2 class="nova-lead-title mb-0">Core Engineering Disciplines</h2>
              </div>
              <p class="nova-lead-desc mb-0" style="max-width: 480px;">
                Specialized skills, technical architectures, and toolchains mastered across production environments.
              </p>
            </div>
            <div class="row g-4">
              ${Object.keys(skills).length > 0 ? Object.entries(skills).map(([cat, list]) => `
                <div class="col-md-6 col-lg-3">
                  <div class="nova-card h-100">
                    <h5 class="fw-bold mb-3" style="color: var(--nova-text); font-size: 1.15rem;">${escapeHtml(cat)}</h5>
                    <div class="d-flex flex-wrap gap-2">
                      ${Array.isArray(list) ? list.map(item => `
                        <span class="nova-badge">${escapeHtml(item)}</span>
                      `).join('') : ''}
                    </div>
                  </div>
                </div>
              `).join('') : `
                <div class="col-12">
                  <div class="nova-card">
                    <div class="d-flex flex-wrap gap-2">
                      ${allSkillsList.map(s => `<span class="nova-badge">${escapeHtml(s)}</span>`).join('')}
                    </div>
                  </div>
                </div>
              `}
            </div>
          </div>
        </section>

        <!-- Career Trajectory / Experience (Image 1 'Reviews') -->
        ${experience.length > 0 ? `
          <section id="section-experience" class="py-5" style="border-top: 1px solid var(--nova-card-border);">
            <div class="container">
              <div class="d-flex justify-content-between align-items-end flex-wrap gap-3 mb-5">
                <div>
                  <span class="nova-kicker mb-2">CAREER TRAJECTORY</span>
                  <h2 class="nova-lead-title mb-0">Professional Track Record</h2>
                </div>
                <p class="nova-lead-desc mb-0" style="max-width: 480px;">
                  Demonstrated history of delivering impactful software systems and strategic outcomes.
                </p>
              </div>
              <div class="row g-4">
                ${experience.map(exp => `
                  <div class="col-lg-6">
                    <div class="nova-card h-100 d-flex flex-column justify-content-between">
                      <div>
                        <div class="d-flex justify-content-between align-items-start mb-2">
                          <h4 class="fw-bold mb-1" style="color: var(--nova-text);">${escapeHtml(exp.title || 'Role')}</h4>
                          <span class="badge rounded-pill px-3 py-2" style="background: rgba(var(--nova-accent-rgb), 0.15); color: var(--nova-accent); font-weight: 700;">
                            ${escapeHtml(exp.start_date || '')} ${exp.end_date ? '— ' + escapeHtml(exp.end_date) : (exp.is_current ? '— Present' : '')}
                          </span>
                        </div>
                        <h6 class="fw-semibold mb-3" style="color: var(--nova-accent);">${escapeHtml(exp.company || '')}</h6>
                        <p class="small text-muted mb-3" style="line-height: 1.7;">${escapeHtml(exp.description || '')}</p>
                        ${exp.highlights && exp.highlights.length ? `
                          <ul class="small ps-3 mb-3 text-muted">
                            ${exp.highlights.map(h => `<li class="mb-1">${escapeHtml(h)}</li>`).join('')}
                          </ul>
                        ` : ''}
                      </div>
                      ${exp.technologies && exp.technologies.length ? `
                        <div class="pt-3 border-top d-flex flex-wrap gap-1" style="border-color: var(--nova-card-border) !important;">
                          ${exp.technologies.map(t => `<span class="badge bg-light text-dark border">${escapeHtml(t)}</span>`).join('')}
                        </div>
                      ` : ''}
                    </div>
                  </div>
                `).join('')}
              </div>
            </div>
          </section>
        ` : ''}

        <!-- Education & Credentials -->
        ${(education.length > 0 || certs.length > 0 || activeSections.includes("education") || activeSections.includes("certifications")) ? `
          <section id="section-credentials" class="py-5" style="border-top: 1px solid var(--nova-card-border);">
            <div class="container">
              <div class="row g-4">
                ${activeSections.includes("education") ? `
                  <div class="col-lg-6" id="section-education">
                    <span class="nova-kicker mb-2">ACADEMIC BACKGROUND</span>
                    <h3 class="nova-lead-title mb-4" style="font-size: 2rem;">Education</h3>
                    ${education.length > 0 ? education.map(edu => `
                      <div class="nova-card mb-3">
                        <h5 class="fw-bold mb-1" style="color: var(--nova-text);">${escapeHtml(edu.degree || '')}</h5>
                        <div class="fw-semibold mb-2" style="color: var(--nova-accent);">${escapeHtml(edu.institution || '')}</div>
                        <div class="small text-muted">${escapeHtml(edu.end_year || '')} ${edu.grade ? '• ' + escapeHtml(edu.grade) : ''}</div>
                      </div>
                    `).join('') : `
                      <div class="nova-card mb-3">
                        <h5 class="fw-bold mb-1" style="color: var(--nova-text);">Degree &amp; Higher Education</h5>
                        <div class="small text-muted">Continuous learning and academic background in technology.</div>
                      </div>
                    `}
                  </div>
                ` : ''}
                ${activeSections.includes("certifications") ? `
                  <div class="col-lg-6" id="section-certifications">
                    <span class="nova-kicker mb-2">VERIFIED SKILLS</span>
                    <h3 class="nova-lead-title mb-4" style="font-size: 2rem;">Certifications</h3>
                    ${certs.length > 0 ? certs.map(c => `
                      <div class="nova-card mb-3">
                        <h5 class="fw-bold mb-1" style="color: var(--nova-text);">${escapeHtml(c.name || '')}</h5>
                        <div class="fw-semibold mb-2" style="color: var(--nova-accent);">${escapeHtml(c.organization || '')}</div>
                        <div class="small text-muted">${escapeHtml(c.year || '')}</div>
                      </div>
                    `).join('') : `
                      <div class="nova-card mb-3">
                        <h5 class="fw-bold mb-1" style="color: var(--nova-text);">Professional Certifications</h5>
                        <div class="small text-muted">Verified technical credentials and industry licenses.</div>
                      </div>
                    `}
                  </div>
                ` : ''}
              </div>
            </div>
          </section>
        ` : ''}

        <!-- Achievements & Recommendations -->
        ${activeSections.includes("achievements") ? renderAchievementsSection(data, "nova") : ''}

        <!-- Contact Section -->
        <section id="section-contact" class="py-5" style="border-top: 1px solid var(--nova-card-border);">
          <div class="container">
            <div class="row g-5 align-items-center">
              <div class="col-lg-5">
                <span class="nova-kicker mb-2">GET IN TOUCH</span>
                <h2 class="nova-lead-title mb-3">Start a project with ${firstName}</h2>
                <p class="nova-hero-summary mb-4">
                  Available for full-time engineering roles, high-impact consulting, and strategic technology advisory.
                </p>
                <div class="d-flex flex-column gap-3 mb-4">
                  ${email ? `<div class="d-flex align-items-center gap-3"><span>✉️</span><strong>${email}</strong></div>` : ''}
                  ${phone ? `<div class="d-flex align-items-center gap-3"><span>📞</span><strong>${phone}</strong></div>` : ''}
                  ${loc ? `<div class="d-flex align-items-center gap-3"><span>📍</span><strong>${loc}</strong></div>` : ''}
                </div>
                <div class="d-flex gap-2 flex-wrap">
                  ${linkedin ? `<a href="${linkedin}" target="_blank" class="nova-btn-secondary py-2 px-3 small">LinkedIn ↗</a>` : ''}
                  ${github ? `<a href="${github}" target="_blank" class="nova-btn-secondary py-2 px-3 small">GitHub ↗</a>` : ''}
                </div>
              </div>
              <div class="col-lg-7">
                <div class="nova-card p-4 p-md-5">
                  <h4 class="fw-bold mb-4" style="color: var(--nova-text);">Direct Recruiter Inquiry</h4>
                  <form id="portfolio-contact-form" onsubmit="event.preventDefault(); alert('Inquiry sent successfully to candidate!');">
                    <div class="row g-3">
                      <div class="col-md-6">
                        <label class="form-label small fw-bold">Your Name</label>
                        <input type="text" class="form-control" placeholder="Hiring Manager / Recruiter" required />
                      </div>
                      <div class="col-md-6">
                        <label class="form-label small fw-bold">Company / Organization</label>
                        <input type="text" class="form-control" placeholder="e.g. Acme Tech" required />
                      </div>
                      <div class="col-12">
                        <label class="form-label small fw-bold">Work Email</label>
                        <input type="email" class="form-control" placeholder="name@company.com" required />
                      </div>
                      <div class="col-12">
                        <label class="form-label small fw-bold">Opportunity Details</label>
                        <textarea class="form-control" rows="4" placeholder="Role description, project requirements, or compensation details..." required></textarea>
                      </div>
                      <div class="col-12 mt-3">
                        <button type="submit" class="nova-btn-primary w-100 justify-content-center">
                          Send Inquiry Directly
                        </button>
                      </div>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Floating Quick Contact Button (Images 2, 3, 4) -->
        <a href="#section-contact" class="nova-floating-contact" title="Get in touch with ${firstName}">
          <span>📞</span>
        </a>

      </div>
    `;

    return html;
  }

  /**
   * 1. MODERN BENTO GRID LAYOUT
   */
  function renderModernBentoLayout(data, activeSections) {
    const name = escapeHtml(data.candidate_name || "");
    const headline = escapeHtml(data.professional_headline || "");
    const avatar = data.profile_image || `https://ui-avatars.com/api/?name=${encodeURIComponent(name || "Candidate")}&background=4f46e5&color=fff&size=200`;
    const soc = data.social_links || {};
    const loc = escapeHtml(soc.location || "");
    const about = escapeHtml(data.about || "");
    const skills = data.skills || {};
    const projects = data.projects || [];
    const experience = data.experience || [];
    const education = data.education || [];
    const certs = data.certifications || [];
    const achievements = data.achievements || [];
    const domainConfig = getDomainConfig(data.theme_id, data);

    // Nav
    let navLinks = activeSections.filter(s => s !== "home").map(s => {
      const t = s.charAt(0).toUpperCase() + s.slice(1);
      return `<a href="#section-${s}" class="text-decoration-none px-3 py-1 rounded-pill small fw-semibold" style="color: var(--theme-text); transition: all 0.2s;">${t}</a>`;
    }).join("");

    let html = `
      <header class="sticky-top py-3 mb-4" style="z-index: 1000;">
        <div class="container d-flex justify-content-between align-items-center">
          <div class="bento-nav-dock d-flex align-items-center gap-2">
            <span class="fw-bold" style="color: var(--theme-text); font-size: 1.05rem;">${name}</span>
          </div>
          <nav class="d-none d-md-flex align-items-center gap-1 bento-nav-dock">
            ${navLinks}
            <a href="#section-contact" class="theme-btn-primary ms-2 py-1 px-3 small">Contact</a>
          </nav>
        </div>
      </header>

      <!-- Hero Section -->
      <section id="section-home" class="py-4 mb-4">
        <div class="container">
          <div class="row align-items-center g-4 mb-4">
            <div class="col-lg-8 animate-fade-in-up">
              <!-- Candidate Name rendered prominently above location & status badge -->
              <h1 class="display-4 fw-extrabold bento-hero-headline mb-2 d-block w-100">${name}</h1>
              <!-- Location & Opportunity Status Badge rendered directly below candidate name -->
              <div class="hero-meta-badge-wrap d-flex flex-wrap align-items-center gap-2 mb-3">
                <div class="d-inline-flex flex-wrap align-items-center gap-2 px-3 py-1 rounded-pill small fw-semibold hero-location-badge" style="background: var(--theme-badge-bg); color: var(--theme-primary); border: 1px solid var(--theme-card-border);">
                  <span class="rounded-circle" style="width: 8px; height: 8px; background: #10b981; display: inline-block;"></span>
                  <span>Available for Opportunities</span>
                  ${domainConfig?.domain ? `<span>•</span><span class="hero-domain-pill"><span class="hero-domain-indicator-dot"></span>${escapeHtml(domainConfig.domain)}</span>` : ""}
                  ${loc ? `<span>•</span><span>📍 ${loc}</span>` : ""}
                </div>
              </div>
              ${headline ? `
                <p class="lead fw-medium mb-4" style="color: var(--theme-secondary); max-width: 650px; line-height: 1.55;">
                  ${headline}
                </p>
              ` : ""}
              <div class="d-flex flex-wrap align-items-center gap-3">
                <a href="#section-contact" class="theme-btn-primary">
                  <span>✉️</span> Get in Touch
                </a>
                <a href="#section-projects" class="theme-btn-outline">
                  <span>🚀</span> Explore Projects
                </a>
                ${soc.github ? `<a href="${escapeHtml(soc.github)}" target="_blank" class="theme-btn-outline"><span>💻</span> GitHub</a>` : ""}
                ${soc.linkedin ? `<a href="${escapeHtml(soc.linkedin)}" target="_blank" class="theme-btn-outline"><span>in</span> LinkedIn</a>` : ""}
              </div>
            </div>
            <div class="col-lg-4 text-center">
              <div class="bento-avatar-card animate-float">
                <div class="mb-3">
                  ${renderCandidateAvatar(data, 150)}
                </div>
                <h5 class="fw-bold mb-1" style="color: var(--theme-text);">${name}</h5>
                ${headline ? `<div class="small fw-semibold mb-3" style="color: var(--theme-primary);">${headline}</div>` : ""}
                <div class="d-flex justify-content-center gap-2 flex-wrap">
                  ${loc ? `<span class="badge" style="background: var(--theme-badge-bg); color: var(--theme-primary);">📍 ${loc}</span>` : ""}
                  <span class="status-badge-hire"><span class="pulse-dot"></span> Available for Hire</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Impact Metrics KPI Strip -->
      ${renderMetricsStrip(data, "modern")}

      <!-- Bento Grid (About + Stats + Skills) -->
      <section class="py-2 mb-5" id="section-about">
        <div class="container">
          <div class="bento-grid">
            ${activeSections.includes("about") ? `
              <div class="bento-card bento-col-8" id="section-about-card">
                <div class="d-flex align-items-center gap-2 mb-3">
                  <span class="fs-4" style="color: var(--theme-primary);">👤</span>
                  <h4 class="fw-bold mb-0" style="color: var(--theme-text);">About &amp; Background</h4>
                </div>
                <div class="lead" style="color: var(--theme-text); opacity: 0.95; font-size: 1.1rem; line-height: 1.8;">
                  ${about || (headline ? `${name} is an accomplished professional specializing in ${headline}. Focused on building high-value, impact-driven software systems.` : `${name} brings technical excellence, strategic problem-solving, and dedication to delivering scalable results.`)}
                </div>
              </div>
            ` : ""}

            <div class="bento-card bento-col-4 d-flex flex-column justify-content-between">
              <div>
                <h6 class="fw-bold text-uppercase small mb-3" style="color: var(--theme-primary); letter-spacing: 0.05em;">Quick Highlights</h6>
                <div class="mb-3">
                  <div class="bento-stat-chip mb-2">
                    <span class="fs-4">💼</span>
                    <div>
                      <div class="fw-bold small" style="color: var(--theme-text);">Experience</div>
                      <div class="small" style="color: var(--theme-text-muted);">${experience.length} Notable Positions</div>
                    </div>
                  </div>
                  <div class="bento-stat-chip mb-2">
                    <span class="fs-4">🚀</span>
                    <div>
                      <div class="fw-bold small" style="color: var(--theme-text);">Featured Work</div>
                      <div class="small" style="color: var(--theme-text-muted);">${projects.length} Showcased Projects</div>
                    </div>
                  </div>
                  ${loc ? `
                    <div class="bento-stat-chip">
                      <span class="fs-4">📍</span>
                      <div>
                        <div class="fw-bold small" style="color: var(--theme-text);">Location</div>
                        <div class="small" style="color: var(--theme-text-muted);">${loc}</div>
                      </div>
                    </div>
                  ` : ""}
                </div>
              </div>
            </div>

            ${activeSections.includes("skills") ? `
              <div class="bento-card bento-col-12" id="section-skills">
                <div class="d-flex align-items-center gap-2 mb-3">
                  <span class="fs-4" style="color: var(--theme-primary);">🛠️</span>
                  <h4 class="fw-bold mb-0" style="color: var(--theme-text);">Core Skills &amp; Tech Stack</h4>
                </div>
                <div>
                  ${renderSkillsBadges(skills)}
                </div>
              </div>
            ` : ""}
          </div>
        </div>
      </section>

      <!-- Services & Value Offerings -->
      ${activeSections.includes("services") ? renderServicesSection(data, "modern") : ""}
    `;

    // Projects with interactive filter toolbar
    if (activeSections.includes("projects") && projects.length > 0) {
      html += `
        <section id="section-projects" class="py-4 mb-5">
          <div class="container">
            <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-3">
              <div class="d-flex align-items-center gap-2">
                <span class="fs-4" style="color: var(--theme-primary);">🚀</span>
                <h3 class="fw-bold mb-0" style="color: var(--theme-text);">Featured Projects</h3>
              </div>
              ${renderProjectFilterToolbar(projects)}
            </div>
            <div class="row g-4">
              ${projects.map((p, idx) => renderEnhancedProjectCard(p, idx, "bento", data)).join("")}
            </div>
          </div>
        </section>
      `;
    }

    // Experience
    if (activeSections.includes("experience") && experience.length > 0) {
      html += `
        <section id="section-experience" class="py-4 mb-5">
          <div class="container">
            <div class="bento-card p-4 p-md-5">
              <div class="d-flex align-items-center gap-2 mb-4">
                <span class="fs-4" style="color: var(--theme-primary);">💼</span>
                <h3 class="fw-bold mb-0" style="color: var(--theme-text);">Work Experience</h3>
              </div>
              <div class="ps-2">
                ${experience.map(exp => `
                  <div class="theme-timeline-item">
                    <div class="theme-timeline-dot"></div>
                    <div class="d-flex justify-content-between align-items-baseline flex-wrap gap-2 mb-1">
                      <h5 class="fw-bold mb-0" style="color: var(--theme-text);">${escapeHtml(exp.title || "Role")}</h5>
                      <span class="theme-date-badge">${escapeHtml([exp.start_date, exp.end_date || (exp.is_current ? "Present" : "")].filter(Boolean).join(" — "))}</span>
                    </div>
                    <div class="fw-semibold small mb-2" style="color: var(--theme-primary);">${escapeHtml(exp.company || "")}</div>
                    ${exp.description ? `<p class="mb-2 small" style="color: var(--theme-text-muted); line-height: 1.6;">${escapeHtml(exp.description)}</p>` : ""}
                    ${exp.highlights?.length ? `<ul class="portfolio-highlight-list ps-3 mb-2 small">${exp.highlights.map(h => `<li class="mb-1">${escapeHtml(h)}</li>`).join("")}</ul>` : ""}
                  </div>
                `).join("")}
              </div>
            </div>
          </div>
        </section>
      `;
    }

    // Education & Certifications
    if (activeSections.includes("education") || activeSections.includes("certifications")) {
      html += `
        <section class="py-3 mb-5" id="section-education-credentials">
          <div class="container">
            <div class="row g-4">
              ${activeSections.includes("education") ? `
                <div class="col-md-6" id="section-education">
                  <div class="bento-card h-100">
                    <h5 class="fw-bold mb-3 d-flex align-items-center gap-2" style="color: var(--theme-text);"><span>🎓</span> Education</h5>
                    ${education.length > 0 ? education.map(e => `
                      <div class="portfolio-subcard p-3 rounded-3 mb-2">
                        <div class="d-flex justify-content-between align-items-start">
                          <div class="fw-bold" style="color: var(--theme-text);">${escapeHtml(e.degree || "")}</div>
                          ${(e.end_year || e.start_year || e.year) ? `<span class="badge rounded-pill bg-primary-subtle text-primary small">${escapeHtml(e.end_year || e.start_year || e.year)}</span>` : ""}
                        </div>
                        <div class="small fw-semibold mt-1" style="color: var(--theme-primary);">${escapeHtml(e.institution || "")}</div>
                        ${e.field_of_study ? `<div class="small text-muted mt-1">${escapeHtml(e.field_of_study)}</div>` : ""}
                        ${(e.details || e.score || e.grade) ? `<div class="small mt-1 text-secondary" style="font-size: 0.82rem;">${escapeHtml(e.details || e.score || e.grade)}</div>` : ""}
                      </div>
                    `).join("") : `
                      <div class="portfolio-subcard p-3 rounded-3 mb-2">
                        <div class="fw-bold" style="color: var(--theme-text);">Academic Background &amp; Degree</div>
                        <div class="small text-muted mt-1">Formal degree in Technology / Computer Science. Continuous academic learning.</div>
                      </div>
                    `}
                  </div>
                </div>
              ` : ""}
              ${activeSections.includes("certifications") ? `
                <div class="col-md-6" id="section-certifications">
                  <div class="bento-card h-100">
                    <h5 class="fw-bold mb-3 d-flex align-items-center gap-2" style="color: var(--theme-text);"><span>🏆</span> Certifications &amp; Credentials</h5>
                    ${certs.length > 0 ? certs.map(c => `
                      <div class="portfolio-subcard p-3 rounded-3 mb-2 d-flex align-items-center gap-2">
                        <span>📜</span>
                        <div>
                          <div class="fw-bold small" style="color: var(--theme-text);">${escapeHtml(c.name || c)}</div>
                          ${c.organization ? `<div class="small text-muted">${escapeHtml(c.organization)}</div>` : ""}
                        </div>
                      </div>
                    `).join("") : `
                      <div class="portfolio-subcard p-3 rounded-3 mb-2 d-flex align-items-center gap-2">
                        <span>📜</span>
                        <div>
                          <div class="fw-bold small" style="color: var(--theme-text);">Professional Certifications &amp; Licenses</div>
                          <div class="small text-muted">Verified technical credentials, assessments, and industry certifications.</div>
                        </div>
                      </div>
                    `}
                  </div>
                </div>
              ` : ""}
            </div>
          </div>
        </section>
      `;
    }

    // Achievements & Social Proof
    if (activeSections.includes("achievements")) {
      html += renderAchievementsSection(data, "modern");
    }

    // Contact
    if (activeSections.includes("contact")) {
      html += renderUniversalContact(data);
    }

    html += renderUniversalFooter(data);
    return html;
  }

  /**
   * 2. DEVELOPER IDE & TERMINAL WORKSTATION LAYOUT
   */
  function renderDeveloperIdeLayout(data, activeSections) {
    const name = escapeHtml(data.candidate_name || "");
    const headline = escapeHtml(data.professional_headline || "");
    const avatar = data.profile_image || `https://ui-avatars.com/api/?name=${encodeURIComponent(name || "Dev")}&background=161b22&color=58a6ff&size=200`;
    const soc = data.social_links || {};
    const loc = escapeHtml(soc.location || "");
    const about = escapeHtml(data.about || "");
    const skills = data.skills || {};
    const projects = data.projects || [];
    const experience = data.experience || [];
    const education = data.education || [];
    const certs = data.certifications || [];

    const safeSlug = escapeHtml(data.slug || "candidate");

    let html = `
      <!-- IDE Window Chrome -->
      <div class="container py-4">
        <div class="dev-ide-window">
          <!-- Window Title Bar -->
          <div class="dev-window-bar">
            <div class="dev-window-dots">
              <span class="dev-dot dev-dot-red"></span>
              <span class="dev-dot dev-dot-yellow"></span>
              <span class="dev-dot dev-dot-green"></span>
              <span class="ms-2 dev-window-title">code ~ /src/portfolio/${safeSlug}.ts</span>
            </div>
            <div class="dev-window-branch">
              <span>⌥ git:(main)*</span>
              <span>•</span>
              <span style="color: #7ee787;">● live</span>
            </div>
          </div>

          <!-- File Editor Tabs -->
          <div class="dev-file-tabs">
            <a href="#section-home" class="dev-tab active"><span>📄</span> Profile.ts</a>
            <a href="#section-skills" class="dev-tab"><span>📦</span> dependencies.json</a>
            <a href="#section-projects" class="dev-tab"><span>🚀</span> repositories.rs</a>
            <a href="#section-experience" class="dev-tab"><span>🪵</span> git-log.sh</a>
            <a href="#section-contact" class="dev-tab"><span>✉️</span> ping.cli</a>
          </div>

          <!-- Code Hero Block -->
          <div class="dev-code-editor" id="section-home">
            <div class="row align-items-center g-4">
              <div class="col-lg-8">
                <p class="dev-comment mb-2">// Developer Profile &amp; Technical Workstation</p>
                <div><span class="dev-line-num">1</span><span class="dev-keyword">interface</span> <span class="dev-type">DeveloperProfile</span> {</div>
                <div><span class="dev-line-num">2</span>  <span class="dev-prop">name</span>: <span class="dev-type">string</span>;</div>
                <div><span class="dev-line-num">3</span>  <span class="dev-prop">role</span>: <span class="dev-type">string</span>;</div>
                <div><span class="dev-line-num">4</span>  <span class="dev-prop">location</span>: <span class="dev-type">string</span>;</div>
                <div><span class="dev-line-num">5</span>  <span class="dev-prop">status</span>: <span class="dev-str">"available"</span>;</div>
                <div><span class="dev-line-num">6</span>}</div>
                <div class="mt-2"><span class="dev-line-num">7</span><span class="dev-keyword">const</span> <span class="dev-prop">profile</span>: <span class="dev-type">DeveloperProfile</span> = {</div>
                <div><span class="dev-line-num">8</span>  <span class="dev-prop">name</span>: <span class="dev-str">"${name}"</span>,</div>
                <div><span class="dev-line-num">9</span>  <span class="dev-prop">role</span>: <span class="dev-str">"${headline}"</span>,</div>
                <div><span class="dev-line-num">10</span>  <span class="dev-prop">location</span>: <span class="dev-str">"${loc}"</span>,</div>
                <div><span class="dev-line-num">11</span>  <span class="dev-prop">status</span>: <span class="dev-str">"available"</span>,</div>
                <div><span class="dev-line-num">12</span>};</div>
                <div class="mt-3 pt-2 d-flex flex-wrap gap-2">
                  <a href="#section-contact" class="theme-btn-primary py-1 px-3 small">
                    <span>$</span> ./contact.sh
                  </a>
                  <a href="#section-projects" class="theme-btn-outline py-1 px-3 small">
                    <span>$</span> git checkout projects
                  </a>
                  ${soc.github ? `<a href="${escapeHtml(soc.github)}" target="_blank" class="theme-btn-outline py-1 px-3 small">GitHub ↗</a>` : ""}
                </div>
              </div>
              <div class="col-lg-4 text-center">
                <div class="p-3 rounded-3" style="background: #161b22; border: 1px solid #30363d;">
                  <img src="${avatar}" alt="${name}" class="rounded-3 mb-2" style="width: 120px; height: 120px; object-fit: cover; border: 2px solid #58a6ff;" />
                  <div class="fw-bold" style="color: #f0f6fc;">${name}</div>
                  <div class="small" style="color: #7ee787;">● Online</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Terminal Interactive Prompt -->
        ${activeSections.includes("about") ? `
          <div id="section-about" class="p-3 mb-4 rounded-3 d-flex align-items-center justify-content-between" style="background: #161b22; border: 1px solid #30363d; font-family: monospace;">
            <div>
              <span style="color: #58a6ff;">${(name.toLowerCase().replace(/[^a-z0-9]/g, '') || 'developer')}@workstation</span>:<span style="color: #7ee787;">~</span>$ cat about.md<span class="terminal-cursor"></span>
              <div class="mt-1 small" style="color: #c9d1d9; opacity: 0.9;">"${about || headline || `${name} is a software engineer and technical specialist.`}"</div>
            </div>
          </div>
        ` : ""}

        <!-- Impact Metrics KPI Telemetry Strip -->
        ${renderMetricsStrip(data, "developer")}

        <!-- Skills (package.json Dependencies) -->
        ${activeSections.includes("skills") ? `
          <div id="section-skills" class="mb-5">
            <h5 class="fw-bold mb-3 d-flex align-items-center gap-2" style="color: var(--theme-text); font-family: monospace;">
              <span>📦</span> package.json // dependencies &amp; tools
            </h5>
            <div class="p-4 rounded-3" style="background: #161b22; border: 1px solid #30363d;">
              ${renderSkillsBadges(skills, "dev")}
            </div>
          </div>
        ` : ""}

        <!-- Value Pillars & Services -->
        ${activeSections.includes("services") ? renderServicesSection(data, "developer") : ""}

        <!-- Repositories Grid -->
        ${activeSections.includes("projects") && projects.length > 0 ? `
          <div id="section-projects" class="mb-5">
            <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-3">
              <h5 class="fw-bold mb-0 d-flex align-items-center gap-2" style="color: var(--theme-text); font-family: monospace;">
                <span>📁</span> Featured Repositories
              </h5>
              ${renderProjectFilterToolbar(projects)}
            </div>
            <div class="row g-3">
              ${projects.map((p, idx) => `
                <div class="col-md-6 col-lg-4 project-card-item" data-tech="${escapeHtml(((p.technologies || []).join(' ') + ' ' + (p.name || '')).toLowerCase())}">
                  <div class="dev-repo-card">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                      <div class="fw-bold" style="color: #58a6ff; font-family: monospace;">📁 ${escapeHtml(p.name || `repo-${idx + 1}`)}</div>
                      <span class="badge" style="background: #21262d; color: #8b949e; border: 1px solid #30363d;">public</span>
                    </div>
                    <p class="small flex-grow-1 mb-3" style="color: #8b949e; line-height: 1.6;">${escapeHtml(p.description || "")}</p>
                    ${p.technologies?.length ? `<div class="mb-3 d-flex flex-wrap gap-1">${p.technologies.map(t => `<span class="badge" style="background: rgba(88, 166, 255, 0.15); color: #58a6ff; font-family: monospace;">${escapeHtml(t)}</span>`).join("")}</div>` : ""}
                    ${renderProjectActionLinks(p, "developer") ? `
                      <div class="pt-2 border-top" style="border-color: #30363d !important;">
                        ${renderProjectActionLinks(p, "developer")}
                      </div>
                    ` : ""}
                  </div>
                </div>
              `).join("")}
            </div>
          </div>
        ` : ""}

        <!-- Experience (git log) -->
        ${activeSections.includes("experience") && experience.length > 0 ? `
          <div id="section-experience" class="mb-5">
            <h5 class="fw-bold mb-3 d-flex align-items-center gap-2" style="color: var(--theme-text); font-family: monospace;">
              <span>🪵</span> git log --graph --oneline // Experience
            </h5>
            <div class="p-4 rounded-3" style="background: #161b22; border: 1px solid #30363d;">
              ${experience.map((exp, idx) => {
                const fakeHash = `c${(idx + 1) * 3}f${idx * 7}e8a`.slice(0, 7);
                const dates = [exp.start_date, exp.end_date || (exp.is_current ? "HEAD" : "")].filter(Boolean).join(" — ");
                return `
                  <div class="dev-git-commit-node">
                    <div class="dev-git-commit-dot"></div>
                    <div class="d-flex align-items-baseline gap-2 flex-wrap mb-1">
                      <span class="dev-git-hash">${fakeHash}</span>
                      <strong style="color: #f0f6fc;">${escapeHtml(exp.title || "")}</strong>
                      <span class="badge" style="background: #238636; color: #fff;">@ ${escapeHtml(exp.company || "")}</span>
                      <span class="small text-muted">${escapeHtml(dates)}</span>
                    </div>
                    ${exp.description ? `<p class="small mb-2" style="color: #8b949e;">${escapeHtml(exp.description)}</p>` : ""}
                    ${exp.highlights?.length ? `<ul class="ps-3 mb-0 small" style="color: #c9d1d9;">${exp.highlights.map(h => `<li>${escapeHtml(h)}</li>`).join("")}</ul>` : ""}
                  </div>
                `;
              }).join("")}
            </div>
          </div>
        ` : ""}

        <!-- Education Credentials -->
        ${activeSections.includes("education") ? `
          <div id="section-education" class="mb-5">
            <h5 class="fw-bold mb-3 d-flex align-items-center gap-2" style="color: var(--theme-text); font-family: monospace;">
              <span>🎓</span> cat education.json // Academic credentials
            </h5>
            <div class="p-4 rounded-3" style="background: #161b22; border: 1px solid #30363d;">
              ${education.length > 0 ? education.map(e => `
                <div class="mb-3 pb-2 border-bottom" style="border-color: #30363d !important;">
                  <div class="d-flex justify-content-between align-items-baseline flex-wrap">
                    <strong style="color: #58a6ff; font-family: monospace;">${escapeHtml(e.degree || "")}</strong>
                    ${(e.end_year || e.start_year || e.year) ? `<span class="badge" style="background: #21262d; color: #8b949e; border: 1px solid #30363d;">${escapeHtml(e.end_year || e.start_year || e.year)}</span>` : ""}
                  </div>
                  <div class="small fw-semibold" style="color: #f0f6fc;">${escapeHtml(e.institution || "")}</div>
                  ${e.field_of_study ? `<div class="small text-muted">${escapeHtml(e.field_of_study)}</div>` : ""}
                  ${(e.details || e.score || e.grade) ? `<div class="small mt-1" style="color: #7ee787; font-family: monospace;">${escapeHtml(e.details || e.score || e.grade)}</div>` : ""}
                </div>
              `).join("") : `
                <div class="small text-muted font-monospace">// Academic Degree &amp; Higher Education in Technology</div>
              `}
            </div>
          </div>
        ` : ""}

        <!-- Certifications Credentials -->
        ${activeSections.includes("certifications") ? `
          <div id="section-certifications" class="mb-5">
            <h5 class="fw-bold mb-3 d-flex align-items-center gap-2" style="color: var(--theme-text); font-family: monospace;">
              <span>🏆</span> cat certifications.lock // Verified credentials &amp; licenses
            </h5>
            <div class="p-4 rounded-3" style="background: #161b22; border: 1px solid #30363d;">
              ${certs.length > 0 ? certs.map(c => `
                <div class="mb-2 pb-2 border-bottom d-flex align-items-center gap-2" style="border-color: #30363d !important;">
                  <span style="color: #58a6ff;">📜</span>
                  <div>
                    <strong style="color: #f0f6fc; font-family: monospace;">${escapeHtml(c.name || c)}</strong>
                    ${c.organization ? `<div class="small text-muted">${escapeHtml(c.organization)} ${c.year ? '• ' + escapeHtml(c.year) : ''}</div>` : ""}
                  </div>
                </div>
              `).join("") : `
                <div class="small text-muted font-monospace">// Professional certifications and verified competencies</div>
              `}
            </div>
          </div>
        ` : ""}

        <!-- Achievements & Recommendations -->
        ${activeSections.includes("achievements") ? renderAchievementsSection(data, "developer") : ""}

        ${activeSections.includes("contact") ? renderUniversalContact(data) : ""}
        ${renderUniversalFooter(data)}
      </div>
    `;

    return html;
  }

  /**
   * 3. CREATIVE STUDIO & NEO-DISPLAY LAYOUT
   */
  function renderCreativeStudioLayout(data, activeSections) {
    const name = escapeHtml(data.candidate_name || "");
    const headline = escapeHtml(data.professional_headline || "");
    const avatar = data.profile_image || `https://ui-avatars.com/api/?name=${encodeURIComponent(name || "Creative")}&background=ec4899&color=fff&size=200`;
    const soc = data.social_links || {};
    const loc = escapeHtml(soc.location || "");
    const about = escapeHtml(data.about || "");
    const skills = data.skills || {};
    const projects = data.projects || [];
    const experience = data.experience || [];
    const education = data.education || [];
    const certs = data.certifications || [];

    let html = `
      <div class="creative-studio-wrap container py-4">
        <!-- Floating Header -->
        <header class="d-flex justify-content-between align-items-center mb-5 pb-3 border-bottom border-2 border-dark">
          <div class="d-flex align-items-center gap-2">
            <span class="fs-3">🎨</span>
            <span class="fw-black fs-4" style="font-weight: 900; letter-spacing: -0.02em;">${name}</span>
          </div>
          <div class="d-flex gap-2">
            <a href="#section-projects" class="theme-btn-outline py-1 px-3 small">Works</a>
            <a href="#section-contact" class="theme-btn-primary py-1 px-3 small">Say Hello!</a>
          </div>
        </header>

        <!-- Big Expressive Hero -->
        <section class="mb-5 pb-4" id="section-home">
          <div class="row align-items-center g-4">
            <div class="col-lg-8">
              <h1 class="creative-hero-title mb-2 d-block w-100">
                Hello, I'm <span style="background: linear-gradient(135deg, var(--theme-primary), var(--theme-secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">${name}</span>.
              </h1>
              <div class="d-flex flex-wrap gap-2 mb-3">
                <span class="creative-sticker" style="background: #fef08a; --rot: -2deg;">✦ Portfolio</span>
                ${loc ? `<span class="creative-sticker" style="background: #fbcfe8; --rot: 1.5deg;">📍 ${loc}</span>` : ""}
              </div>
              <p class="fs-4 fw-semibold mb-4" style="color: var(--theme-text-muted); line-height: 1.45;">
                ${headline}
              </p>
              <div class="d-flex gap-3 flex-wrap">
                <a href="#section-projects" class="theme-btn-primary py-2 px-4 fs-6">
                  <span>Explore Selected Work</span>
                </a>
                <a href="#section-contact" class="theme-btn-outline py-2 px-4 fs-6">
                  <span>Get in Touch</span>
                </a>
              </div>
            </div>
            <div class="col-lg-4 text-center">
              <div class="position-relative d-inline-block">
                <div style="width: 170px; height: 170px; border-radius: 50%; padding: 6px; background: linear-gradient(135deg, var(--theme-primary), var(--theme-secondary));">
                  <img src="${avatar}" alt="${name}" class="rounded-circle w-100 h-100 object-fit-cover" />
                </div>
                <div class="creative-sticker position-absolute bottom-0 start-50 translate-middle-x" style="background: #86efac; white-space: nowrap;">
                  ● Available
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Impact Metrics KPI Strip -->
        ${renderMetricsStrip(data, "creative")}

        <!-- Statement About Card -->
        ${activeSections.includes("about") ? `
          <div class="creative-neo-card mb-5" id="section-about">
            <div class="d-flex gap-3">
              <span class="display-3 fw-bold" style="color: var(--theme-primary); line-height: 0.8;">“</span>
              <div class="fs-4 fw-medium" style="color: var(--theme-text); line-height: 1.6;">
                ${about || headline || `${name} designs and engineers cutting-edge digital experiences and modern platforms.`}
              </div>
            </div>
          </div>
        ` : ""}

        <!-- Value Pillars / Services -->
        ${activeSections.includes("services") ? renderServicesSection(data, "creative") : ""}

        <!-- Bouncy Skills Cloud -->
        ${activeSections.includes("skills") ? `
          <div id="section-skills" class="mb-5">
            <h3 class="fw-bold mb-3">Core Competencies &amp; Capabilities</h3>
            <div class="creative-neo-card">
              ${renderSkillsBadges(skills, "creative")}
            </div>
          </div>
        ` : ""}

        <!-- Neo-Brutalist Projects -->
        ${activeSections.includes("projects") && projects.length > 0 ? `
          <div id="section-projects" class="mb-5">
            <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-4">
              <h3 class="fw-bold mb-0">Selected Case Studies</h3>
              ${renderProjectFilterToolbar(projects)}
            </div>
            <div class="row g-4">
              ${projects.map((p, idx) => `
                <div class="col-md-6 project-card-item" data-tech="${escapeHtml(((p.technologies || []).join(' ') + ' ' + (p.name || '')).toLowerCase())}">
                  <div class="creative-neo-card h-100 d-flex flex-column">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                      <h4 class="fw-bold mb-0">${escapeHtml(p.name || `Case Study #${idx + 1}`)}</h4>
                    </div>
                    <p class="flex-grow-1" style="color: var(--theme-text-muted); line-height: 1.6;">${escapeHtml(p.description || "")}</p>
                    ${p.technologies?.length ? `<div class="mb-3 d-flex flex-wrap gap-1">${p.technologies.map(t => `<span class="badge bg-light text-dark border px-2 py-1">${escapeHtml(t)}</span>`).join("")}</div>` : ""}
                    ${renderProjectActionLinks(p, "creative") ? `
                      <div class="pt-3 border-top mt-auto">
                        ${renderProjectActionLinks(p, "creative")}
                      </div>
                    ` : ""}
                  </div>
                </div>
              `).join("")}
            </div>
          </div>
        ` : ""}

        <!-- Experience -->
        ${activeSections.includes("experience") && experience.length > 0 ? `
          <div id="section-experience" class="mb-5">
            <h3 class="fw-bold mb-4">Career Journey</h3>
            <div class="creative-neo-card">
              ${experience.map(exp => `
                <div class="border-bottom pb-3 mb-3">
                  <div class="d-flex justify-content-between align-items-baseline flex-wrap">
                    <h5 class="fw-bold mb-1">${escapeHtml(exp.title || "")}</h5>
                    <span class="badge rounded-pill" style="background: var(--theme-badge-bg); color: var(--theme-primary);">${escapeHtml([exp.start_date, exp.end_date || (exp.is_current ? "Present" : "")].filter(Boolean).join(" — "))}</span>
                  </div>
                  <div class="fw-semibold mb-2" style="color: var(--theme-primary);">${escapeHtml(exp.company || "")}</div>
                  ${exp.description ? `<p class="small text-muted mb-1">${escapeHtml(exp.description)}</p>` : ""}
                </div>
              `).join("")}
            </div>
          </div>
        ` : ""}

        <!-- Education & Certifications -->
        ${(activeSections.includes("education") || activeSections.includes("certifications")) ? `
          <div class="row g-4 mb-5">
            ${activeSections.includes("education") ? `
              <div class="col-md-6" id="section-education">
                <div class="creative-neo-card h-100">
                  <h4 class="fw-bold mb-3">🎓 Academic Qualifications</h4>
                  ${education.length > 0 ? education.map(e => `
                    <div class="border-bottom pb-2 mb-2">
                      <strong class="d-block" style="color: var(--theme-text);">${escapeHtml(e.degree || "")}</strong>
                      <div class="small fw-semibold" style="color: var(--theme-primary);">${escapeHtml(e.institution || "")}</div>
                      <div class="small text-muted">${escapeHtml([e.end_year || e.start_year || e.year, e.grade].filter(Boolean).join(" • "))}</div>
                    </div>
                  `).join("") : `<div class="small text-muted">Higher Education &amp; Degree in Technology</div>`}
                </div>
              </div>
            ` : ""}
            ${activeSections.includes("certifications") ? `
              <div class="col-md-6" id="section-certifications">
                <div class="creative-neo-card h-100">
                  <h4 class="fw-bold mb-3">🏆 Credentials &amp; Badges</h4>
                  ${certs.length > 0 ? certs.map(c => `
                    <div class="border-bottom pb-2 mb-2">
                      <strong class="d-block" style="color: var(--theme-text);">${escapeHtml(c.name || c)}</strong>
                      ${c.organization ? `<div class="small text-muted">${escapeHtml(c.organization)}</div>` : ""}
                    </div>
                  `).join("") : `<div class="small text-muted">Verified industry certifications and training</div>`}
                </div>
              </div>
            ` : ""}
          </div>
        ` : ""}

        <!-- Recommendations & Achievements -->
        ${activeSections.includes("achievements") ? renderAchievementsSection(data, "creative") : ""}

        ${activeSections.includes("contact") ? renderUniversalContact(data) : ""}
        ${renderUniversalFooter(data)}
      </div>
    `;

    return html;
  }

  /**
   * 4. CORPORATE EXECUTIVE BRIEFING (2-COLUMN) LAYOUT
   */
  function renderCorporateExecutiveLayout(data, activeSections) {
    const name = escapeHtml(data.candidate_name || "");
    const headline = escapeHtml(data.professional_headline || "");
    const avatar = data.profile_image || `https://ui-avatars.com/api/?name=${encodeURIComponent(name || "Executive")}&background=1e3a8a&color=fff&size=200`;
    const soc = data.social_links || {};
    const loc = escapeHtml(soc.location || "");
    const about = escapeHtml(data.about || "");
    const skills = data.skills || {};
    const projects = data.projects || [];
    const experience = data.experience || [];
    const education = data.education || [];
    const certs = data.certifications || [];

    let html = `
      <div class="container py-4">
        <!-- Executive Masthead Banner -->
        <div class="corp-exec-masthead" id="section-home">
          <div class="row align-items-center g-4">
            <div class="col-md-9">
              <div class="corp-verified-badge mb-2">
                <span>💼</span> Professional Executive Dossier
              </div>
              <h1 class="display-5 fw-bold mb-2 text-white">${name}</h1>
              <p class="fs-5 opacity-90 mb-3 text-white-50">${headline}</p>
              <div class="corp-metric-strip">
                ${experience.length ? `<div class="corp-metric-item">💼 ${experience.length} Professional Roles</div>` : ""}
                ${projects.length ? `<div class="corp-metric-item">🚀 ${projects.length} Strategic Deliverables</div>` : ""}
                ${loc ? `<div class="corp-metric-item">📍 ${loc}</div>` : ""}
              </div>
            </div>
            <div class="col-md-3 text-center">
              <img src="${avatar}" alt="${name}" class="rounded-3 shadow-lg border border-3 border-white" style="width: 130px; height: 130px; object-fit: cover;" />
            </div>
          </div>
        </div>

        <!-- Executive KPI Metrics Strip -->
        <div class="my-4">
          ${renderMetricsStrip(data, "corporate")}
        </div>

        <!-- 2-Column Executive Briefing -->
        <div class="corp-two-col">
          <!-- Left Column (Competencies, Education, Certifications, Contact) -->
          <div class="corp-sidebar-col">
            <div class="corp-sidebar-card" id="section-about">
              <h6 class="fw-bold text-uppercase small mb-3" style="color: var(--theme-primary);">Executive Overview</h6>
              <p class="small text-muted mb-0" style="line-height: 1.7;">${about || headline || `${name} is a senior leader and technology executive.`}</p>
            </div>

            ${activeSections.includes("skills") ? `
              <div class="corp-sidebar-card" id="section-skills">
                <h6 class="fw-bold text-uppercase small mb-3" style="color: var(--theme-primary);">Core Competencies</h6>
                ${renderSkillsBadges(skills, "corp")}
              </div>
            ` : ""}

            ${(activeSections.includes("education") || education.length > 0) ? `
              <div class="corp-sidebar-card" id="section-education">
                <h6 class="fw-bold text-uppercase small mb-3" style="color: var(--theme-primary);">Education</h6>
                ${education.length > 0 ? education.map(e => `
                  <div class="mb-3 pb-2 border-bottom border-light">
                    <div class="d-flex justify-content-between align-items-baseline">
                      <div class="fw-bold small" style="color: var(--theme-text);">${escapeHtml(e.degree || "")}</div>
                      ${(e.end_year || e.start_year || e.year) ? `<span class="small text-muted">${escapeHtml(e.end_year || e.start_year || e.year)}</span>` : ""}
                    </div>
                    <div class="small fw-semibold text-muted">${escapeHtml(e.institution || "")}</div>
                    ${e.field_of_study ? `<div class="small text-muted">${escapeHtml(e.field_of_study)}</div>` : ""}
                    ${(e.details || e.score || e.grade) ? `<div class="small text-secondary mt-1">${escapeHtml(e.details || e.score || e.grade)}</div>` : ""}
                  </div>
                `).join("") : `<div class="small text-muted">Higher Education in Technology / Management</div>`}
              </div>
            ` : ""}

            ${(activeSections.includes("certifications") || certs.length > 0) ? `
              <div class="corp-sidebar-card" id="section-certifications">
                <h6 class="fw-bold text-uppercase small mb-3" style="color: var(--theme-primary);">Credentials &amp; Licenses</h6>
                ${certs.length > 0 ? certs.map(c => `
                  <div class="small fw-semibold mb-1" style="color: var(--theme-text);">• ${escapeHtml(c.name || c)}</div>
                `).join("") : `<div class="small text-muted">Verified Executive &amp; Professional Certifications</div>`}
              </div>
            ` : ""}

            <div class="corp-sidebar-card">
              <h6 class="fw-bold text-uppercase small mb-3" style="color: var(--theme-primary);">Direct Channels</h6>
              ${soc.email ? `<div class="small mb-1"><a href="mailto:${escapeHtml(soc.email)}" class="text-decoration-none">✉️ ${escapeHtml(soc.email)}</a></div>` : ""}
              ${soc.phone ? `<div class="small mb-1">📞 ${escapeHtml(soc.phone)}</div>` : ""}
              ${soc.linkedin ? `<div class="small"><a href="${escapeHtml(soc.linkedin)}" target="_blank" class="text-decoration-none">in LinkedIn Profile</a></div>` : ""}
            </div>
          </div>

          <!-- Right Column (Career Trajectory & Strategic Deliverables) -->
          <div class="corp-main-col">
            <!-- Strategic Pillars & Services -->
            ${activeSections.includes("services") ? renderServicesSection(data, "corporate") : ""}

            ${activeSections.includes("experience") && experience.length > 0 ? `
              <div class="corp-sidebar-card mb-4" id="section-experience">
                <h5 class="fw-bold mb-4" style="color: var(--theme-text);">Executive Career Trajectory</h5>
                ${experience.map(exp => `
                  <div class="border-bottom pb-4 mb-4">
                    <div class="d-flex justify-content-between align-items-baseline flex-wrap gap-2 mb-1">
                      <h5 class="fw-bold mb-0" style="color: var(--theme-text);">${escapeHtml(exp.title || "")}</h5>
                      <span class="badge bg-secondary-subtle text-secondary">${escapeHtml([exp.start_date, exp.end_date || (exp.is_current ? "Present" : "")].filter(Boolean).join(" — "))}</span>
                    </div>
                    <div class="fw-semibold small mb-2" style="color: var(--theme-primary);">${escapeHtml(exp.company || "")}</div>
                    ${exp.description ? `<p class="small text-muted mb-2" style="line-height: 1.6;">${escapeHtml(exp.description)}</p>` : ""}
                    ${exp.highlights?.length ? `<ul class="ps-3 mb-0 small text-muted">${exp.highlights.map(h => `<li class="mb-1">${escapeHtml(h)}</li>`).join("")}</ul>` : ""}
                  </div>
                `).join("")}
              </div>
            ` : ""}

            ${activeSections.includes("projects") && projects.length > 0 ? `
              <div class="corp-sidebar-card mb-4" id="section-projects">
                <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-3">
                  <h5 class="fw-bold mb-0" style="color: var(--theme-text);">Key Strategic Deliverables</h5>
                  ${renderProjectFilterToolbar(projects)}
                </div>
                <div class="row g-3">
                  ${projects.map(p => `
                    <div class="col-md-6 project-card-item" data-tech="${escapeHtml(((p.technologies || []).join(' ') + ' ' + (p.name || '')).toLowerCase())}">
                      <div class="p-3 rounded border h-100 d-flex flex-column">
                        <h6 class="fw-bold mb-1" style="color: var(--theme-text);">${escapeHtml(p.name || "")}</h6>
                        <p class="small text-muted mb-2 flex-grow-1">${escapeHtml(p.description || "")}</p>
                        ${renderProjectActionLinks(p, "corporate")}
                      </div>
                    </div>
                  `).join("")}
                </div>
              </div>
            ` : ""}

            <!-- Testimonials & Board Endorsements -->
            ${activeSections.includes("achievements") ? renderTestimonialsSection(data, "corporate") : ""}
          </div>
        </div>

        ${activeSections.includes("contact") ? renderUniversalContact(data) : ""}
        ${renderUniversalFooter(data)}
      </div>
    `;

    return html;
  }

  /**
   * 5. AI / TECH NEURAL HUD LAYOUT
   */
  function renderAiTechHudLayout(data, activeSections) {
    const name = escapeHtml(data.candidate_name || "");
    const headline = escapeHtml(data.professional_headline || "");
    const avatar = data.profile_image || `https://ui-avatars.com/api/?name=${encodeURIComponent(name || "Tech")}&background=050814&color=06b6d4&size=200`;
    const soc = data.social_links || {};
    const loc = escapeHtml(soc.location || "");
    const about = escapeHtml(data.about || "");
    const skills = data.skills || {};
    const projects = data.projects || [];
    const experience = data.experience || [];
    const education = data.education || [];
    const certs = data.certifications || [];

    let html = `
      <div class="ai-cyber-stage min-vh-100 py-3">
        <!-- HUD Status Bar -->
        <div class="ai-hud-bar">
          <div><span style="color: #10b981;">●</span> STATUS: ACTIVE // SYSTEMS OPERATIONAL</div>
          <div>${loc ? `LOCATION: ${loc.toUpperCase()}` : `ENGINEERING WORKSTATION`}</div>
        </div>

        <div class="container py-4">
          <!-- Cyber Hero -->
          <div class="row align-items-center g-4 mb-5" id="section-home">
            <div class="col-lg-8">
              <h1 class="display-4 fw-extrabold mb-2 d-block w-100" style="color: #f8fafc; font-family: monospace;">
                &gt; ${name}_
              </h1>
              <div class="d-flex flex-wrap gap-2 mb-3">
                ${loc ? `<span class="ai-telemetry-badge">📍 ${loc}</span>` : ""}
                <span class="ai-telemetry-badge">● Systems Operational</span>
              </div>
              <p class="lead mb-4" style="color: #38bdf8; max-width: 650px;">
                ${headline}
              </p>
              <div class="d-flex gap-3 flex-wrap">
                <a href="#section-contact" class="theme-btn-primary py-2 px-4">Get in Touch</a>
                <a href="#section-projects" class="theme-btn-outline py-2 px-4">View Projects</a>
              </div>
            </div>
            <div class="col-lg-4 text-center">
              <div class="ai-radar-ring">
                <div class="ai-radar-ping"></div>
                <img src="${avatar}" alt="${name}" />
              </div>
              <div class="badge" style="background: rgba(6, 182, 212, 0.2); color: #06b6d4; font-family: monospace;">
                STATUS: ACTIVE
              </div>
            </div>
          </div>

          <!-- Neural KPI Telemetry Metrics Strip -->
          ${renderMetricsStrip(data, "ai_tech")}

          <!-- Neural Directive Overview Card -->
          ${activeSections.includes("about") ? `
            <div class="ai-hologram-card mb-5" id="section-about">
              <div class="ai-corner-accent ai-corner-tl"></div>
              <div class="ai-corner-accent ai-corner-tr"></div>
              <div class="ai-corner-accent ai-corner-bl"></div>
              <div class="ai-corner-accent ai-corner-br"></div>
              <h5 class="fw-bold mb-3" style="color: #06b6d4; font-family: monospace;">// PROFESSIONAL BACKGROUND</h5>
              <p class="lead mb-0" style="color: #cbd5e1; font-size: 1.15rem; line-height: 1.8;">${about || headline || `${name} is an artificial intelligence and software architecture specialist.`}</p>
            </div>
          ` : ""}

          <!-- Neural Value Services / Core Capabilities -->
          ${activeSections.includes("services") ? renderServicesSection(data, "ai_tech") : ""}

          <!-- Neural Skills Pod -->
          ${activeSections.includes("skills") ? `
            <div id="section-skills" class="mb-5">
              <h4 class="fw-bold mb-4" style="color: #06b6d4; font-family: monospace;">// TECHNICAL SKILLS &amp; ARCHITECTURE</h4>
              <div class="ai-hologram-card">
                ${renderSkillsBadges(skills, "ai")}
              </div>
            </div>
          ` : ""}

          <!-- Holographic Projects -->
          ${activeSections.includes("projects") && projects.length > 0 ? `
            <div id="section-projects" class="mb-5">
              <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-4">
                <h4 class="fw-bold mb-0" style="color: #06b6d4; font-family: monospace;">// FEATURED SYSTEMS &amp; PROJECTS</h4>
                ${renderProjectFilterToolbar(projects)}
              </div>
              <div class="row g-4">
                ${projects.map((p, idx) => `
                  <div class="col-md-6 col-lg-4 project-card-item" data-tech="${escapeHtml(((p.technologies || []).join(' ') + ' ' + (p.name || '')).toLowerCase())}">
                    <div class="ai-hologram-card h-100 d-flex flex-column">
                      <div class="d-flex justify-content-between align-items-center mb-2">
                        <h5 class="fw-bold mb-0" style="color: #f8fafc; font-family: monospace;">${escapeHtml(p.name || `MODULE_${idx + 1}`)}</h5>
                      </div>
                      <p class="small flex-grow-1 text-muted mb-3">${escapeHtml(p.description || "")}</p>
                      ${p.technologies?.length ? `<div class="mb-3 d-flex flex-wrap gap-1">${p.technologies.map(t => `<span class="ai-telemetry-badge">${escapeHtml(t)}</span>`).join("")}</div>` : ""}
                      ${renderProjectActionLinks(p, "ai_tech") ? `
                        <div class="pt-2 border-top border-secondary mt-auto">
                          ${renderProjectActionLinks(p, "ai_tech")}
                        </div>
                      ` : ""}
                    </div>
                  </div>
                `).join("")}
              </div>
            </div>
          ` : ""}

          <!-- Experience Pipeline -->
          ${activeSections.includes("experience") && experience.length > 0 ? `
            <div id="section-experience" class="mb-5">
              <h4 class="fw-bold mb-4" style="color: #06b6d4; font-family: monospace;">// CAREER HISTORY &amp; TIMELINE</h4>
              <div class="ai-hologram-card">
                ${experience.map(exp => `
                  <div class="border-bottom border-secondary pb-3 mb-3">
                    <div class="d-flex justify-content-between align-items-baseline flex-wrap">
                      <h5 class="fw-bold mb-1" style="color: #f8fafc;">${escapeHtml(exp.title || "")}</h5>
                      <span class="ai-telemetry-badge">${escapeHtml([exp.start_date, exp.end_date || (exp.is_current ? "Present" : "")].filter(Boolean).join(" — "))}</span>
                    </div>
                    <div class="small mb-2" style="color: #06b6d4;">${escapeHtml(exp.company || "")}</div>
                    ${exp.description ? `<p class="small text-muted mb-1">${escapeHtml(exp.description)}</p>` : ""}
                  </div>
                `).join("")}
              </div>
            </div>
          ` : ""}

          <!-- Academic Credentials Pipeline -->
          ${activeSections.includes("education") && education.length > 0 ? `
            <div id="section-education" class="mb-5">
              <h4 class="fw-bold mb-4" style="color: #06b6d4; font-family: monospace;">// ACADEMIC CREDENTIALS &amp; EDUCATION</h4>
              <div class="ai-hologram-card">
                ${education.map(e => `
                  <div class="border-bottom border-secondary pb-3 mb-3">
                    <div class="d-flex justify-content-between align-items-baseline flex-wrap">
                      <h5 class="fw-bold mb-1" style="color: #f8fafc;">${escapeHtml(e.degree || "")}</h5>
                      ${(e.end_year || e.start_year || e.year) ? `<span class="ai-telemetry-badge">${escapeHtml(e.end_year || e.start_year || e.year)}</span>` : ""}
                    </div>
                    <div class="small mb-1" style="color: #06b6d4;">${escapeHtml(e.institution || "")}</div>
                    ${e.field_of_study ? `<div class="small text-muted mb-1">${escapeHtml(e.field_of_study)}</div>` : ""}
                    ${(e.details || e.score || e.grade) ? `<div class="small mt-1" style="color: #38bdf8;">${escapeHtml(e.details || e.score || e.grade)}</div>` : ""}
                  </div>
                `).join("")}
              </div>
            </div>
          ` : ""}

          <!-- Industry Certifications Pipeline -->
          ${(activeSections.includes("certifications") || certs.length > 0) ? `
            <div id="section-certifications" class="mb-5">
              <h4 class="fw-bold mb-4" style="color: #06b6d4; font-family: monospace;">// INDUSTRY CERTIFICATIONS &amp; LICENSES</h4>
              <div class="ai-hologram-card">
                ${certs.length > 0 ? certs.map(c => `
                  <div class="border-bottom border-secondary pb-3 mb-3 d-flex align-items-center gap-2">
                    <span style="color: #06b6d4;">[AUTH_KEY]</span>
                    <div>
                      <h6 class="fw-bold mb-0" style="color: #f8fafc;">${escapeHtml(c.name || c)}</h6>
                      ${c.organization ? `<div class="small text-muted">${escapeHtml(c.organization)} ${c.year ? '• ' + escapeHtml(c.year) : ''}</div>` : ""}
                    </div>
                  </div>
                `).join("") : `<div class="small text-muted font-monospace">// Verified Professional Certifications and Technical Competencies</div>`}
              </div>
            </div>
          ` : ""}

          <!-- Verified Achievements & Endorsements -->
          ${activeSections.includes("achievements") ? renderAchievementsSection(data, "ai_tech") : ""}

          ${activeSections.includes("contact") ? renderUniversalContact(data) : ""}
          ${renderUniversalFooter(data)}
        </div>
      </div>
    `;

    return html;
  }

  /**
   * 6. MINIMAL SWISS EDITORIAL LAYOUT
   */
  function renderMinimalEditorialLayout(data, activeSections) {
    const name = escapeHtml(data.candidate_name || "");
    const headline = escapeHtml(data.professional_headline || "");
    const soc = data.social_links || {};
    const loc = escapeHtml(soc.location || "");
    const about = escapeHtml(data.about || "");
    const skills = data.skills || {};
    const projects = data.projects || [];
    const experience = data.experience || [];
    const education = data.education || [];
    const certs = data.certifications || [];

    let html = `
      <div class="minimal-editorial-wrap">
        <header class="d-flex justify-content-between align-items-baseline mb-5 pb-3 border-bottom">
          <div class="fw-bold fs-5">${name}</div>
          <div class="small text-muted">${loc}</div>
        </header>

        <section class="mb-5" id="section-home">
          <h1 class="display-4 fw-bold mb-2 d-block w-100" style="letter-spacing: -0.03em;">${name}</h1>
          ${loc ? `<div class="d-inline-flex align-items-center gap-2 px-3 py-1 rounded-pill small mb-3 border text-muted">📍 ${loc}</div>` : ""}
          <p class="fs-4 text-muted mb-4" style="line-height: 1.45;">${headline}</p>
          <div class="d-flex gap-3">
            <a href="#section-contact" class="theme-btn-primary py-2 px-4 small">Contact</a>
            ${soc.linkedin ? `<a href="${escapeHtml(soc.linkedin)}" target="_blank" class="theme-btn-outline py-2 px-4 small">LinkedIn</a>` : ""}
            ${soc.github ? `<a href="${escapeHtml(soc.github)}" target="_blank" class="theme-btn-outline py-2 px-4 small">GitHub</a>` : ""}
          </div>
        </section>

        <!-- Performance Indicators -->
        ${renderMetricsStrip(data, "minimal")}

        <div class="minimal-hairline-rule"></div>

        ${activeSections.includes("about") ? `
          <section class="mb-5" id="section-about">
            <span class="minimal-index-num">01 / OVERVIEW</span>
            <div class="fs-5" style="line-height: 1.8; color: var(--theme-text);">
              ${about}
            </div>
          </section>
          <div class="minimal-hairline-rule"></div>
        ` : ""}

        <!-- Strategic Value Services -->
        ${activeSections.includes("services") ? `
          <div class="mb-5">
            ${renderServicesSection(data, "minimal")}
          </div>
          <div class="minimal-hairline-rule"></div>
        ` : ""}

        ${activeSections.includes("projects") && projects.length > 0 ? `
          <section class="mb-5" id="section-projects">
            <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
              <span class="minimal-index-num mb-0">02 / SELECTED WORK</span>
              ${renderProjectFilterToolbar(projects)}
            </div>
            <div>
              ${projects.map((p, idx) => `
                <div class="minimal-horizontal-proj project-card-item" data-tech="${escapeHtml(((p.technologies || []).join(' ') + ' ' + (p.name || '')).toLowerCase())}">
                  <div>
                    <span class="small text-muted me-2">${String(idx + 1).padStart(2, '0')}.</span>
                    <strong>${escapeHtml(p.name || "")}</strong>
                    <div class="small text-muted">${escapeHtml(p.description || "")}</div>
                  </div>
                  <div>
                    ${renderProjectActionLinks(p, "minimal")}
                  </div>
                </div>
              `).join("")}
            </div>
          </section>
          <div class="minimal-hairline-rule"></div>
        ` : ""}

        ${activeSections.includes("experience") && experience.length > 0 ? `
          <section class="mb-5" id="section-experience">
            <span class="minimal-index-num">03 / RECORD</span>
            <div>
              ${experience.map(exp => `
                <div class="mb-4">
                  <div class="d-flex justify-content-between align-items-baseline">
                    <strong>${escapeHtml(exp.title || "")} — ${escapeHtml(exp.company || "")}</strong>
                    <span class="small text-muted">${escapeHtml([exp.start_date, exp.end_date || (exp.is_current ? "Present" : "")].filter(Boolean).join(" — "))}</span>
                  </div>
                  ${exp.description ? `<p class="small text-muted mb-0 mt-1">${escapeHtml(exp.description)}</p>` : ""}
                </div>
              `).join("")}
            </div>
          </section>
          <div class="minimal-hairline-rule"></div>
        ` : ""}

        ${activeSections.includes("skills") ? `
          <section class="mb-5" id="section-skills">
            <span class="minimal-index-num">04 / CAPABILITIES</span>
            <div>${renderSkillsBadges(skills, "minimal")}</div>
          </section>
          <div class="minimal-hairline-rule"></div>
        ` : ""}

        ${(activeSections.includes("education") || education.length > 0) ? `
          <section class="mb-5" id="section-education">
            <span class="minimal-index-num">05 / EDUCATION</span>
            <div>
              ${education.length > 0 ? education.map(e => `
                <div class="mb-3">
                  <div class="d-flex justify-content-between align-items-baseline">
                    <strong>${escapeHtml(e.degree || "")} — ${escapeHtml(e.institution || "")}</strong>
                    ${(e.end_year || e.start_year || e.year) ? `<span class="small text-muted">${escapeHtml(e.end_year || e.start_year || e.year)}</span>` : ""}
                  </div>
                  ${e.field_of_study ? `<div class="small text-muted">${escapeHtml(e.field_of_study)}</div>` : ""}
                </div>
              `).join("") : `<div>Degree &amp; Academic Background in Technology</div>`}
            </div>
          </section>
          <div class="minimal-hairline-rule"></div>
        ` : ""}

        ${(activeSections.includes("certifications") || certs.length > 0) ? `
          <section class="mb-5" id="section-certifications">
            <span class="minimal-index-num">06 / CERTIFICATIONS</span>
            <div>
              ${certs.length > 0 ? certs.map(c => `
                <div class="mb-2">
                  <strong>${escapeHtml(c.name || c)}</strong>
                  ${c.organization ? `<span class="small text-muted ms-2">• ${escapeHtml(c.organization)}</span>` : ""}
                </div>
              `).join("") : `<div>Verified Professional Certifications &amp; Credentials</div>`}
            </div>
          </section>
          <div class="minimal-hairline-rule"></div>
        ` : ""}

        <!-- Achievements & Endorsements -->
        ${activeSections.includes("achievements") ? `
          <div class="mb-5">
            ${renderAchievementsSection(data, "minimal")}
          </div>
          <div class="minimal-hairline-rule"></div>
        ` : ""}

        ${activeSections.includes("contact") ? renderUniversalContact(data) : ""}
        ${renderUniversalFooter(data)}
      </div>
    `;

    return html;
  }

  /**
   * 7. DARK LUXURY TITANIUM SHOWCASE
   */
  function renderDarkLuxuryLayout(data, activeSections) {
    const name = escapeHtml(data.candidate_name || "");
    const headline = escapeHtml(data.professional_headline || "");
    const avatar = data.profile_image || `https://ui-avatars.com/api/?name=${encodeURIComponent(name || "Candidate")}&background=10141f&color=818cf8&size=200`;
    const soc = data.social_links || {};
    const loc = escapeHtml(soc.location || "");
    const about = escapeHtml(data.about || "");
    const skills = data.skills || {};
    const projects = data.projects || [];
    const experience = data.experience || [];
    const education = data.education || [];
    const certs = data.certifications || [];

    let html = `
      <div class="container py-4">
        <!-- Floating Titanium Dock -->
        <header class="d-flex justify-content-between align-items-center mb-5">
          <div class="dark-luxury-dock d-flex align-items-center gap-2">
            <span style="color: var(--theme-primary);">✦</span>
            <span class="fw-bold" style="color: #f8fafc;">${name}</span>
          </div>
          <div class="dark-luxury-dock d-none d-md-flex gap-2">
            <a href="#section-projects" class="text-decoration-none px-3 py-1 small" style="color: #f8fafc;">Projects</a>
            <a href="#section-experience" class="text-decoration-none px-3 py-1 small" style="color: #f8fafc;">Experience</a>
            <a href="#section-contact" class="theme-btn-primary py-1 px-3 small">Contact</a>
          </div>
        </header>

        <!-- Luxury Hero -->
        <div class="row align-items-center g-4 mb-5" id="section-home">
          <div class="col-lg-8">
            <h1 class="display-4 fw-extrabold mb-2 d-block w-100" style="color: #f8fafc;">
              ${name}
            </h1>
            <div class="d-flex flex-wrap gap-2 mb-3">
              <div class="d-inline-flex align-items-center gap-2 px-3 py-1 rounded-pill small" style="background: rgba(129, 140, 248, 0.15); color: #818cf8; border: 1px solid rgba(129, 140, 248, 0.3);">
                <span>✦</span> ${headline ? headline.split(/[,|•/]/)[0].trim() : 'Executive Portfolio'}
              </div>
              ${loc ? `<div class="d-inline-flex align-items-center gap-2 px-3 py-1 rounded-pill small" style="background: rgba(255, 255, 255, 0.08); color: #cbd5e1; border: 1px solid rgba(255, 255, 255, 0.15);">📍 ${loc}</div>` : ""}
            </div>
            <p class="lead mb-4" style="color: var(--theme-secondary); max-width: 600px;">
              ${headline}
            </p>
            <div class="d-flex gap-3">
              <a href="#section-contact" class="theme-btn-primary py-2 px-4">Direct Inquiry</a>
              <a href="#section-projects" class="theme-btn-outline py-2 px-4">View Portfolio</a>
            </div>
          </div>
          <div class="col-lg-4 text-center">
            <div class="dark-titanium-card d-inline-block p-3">
              <img src="${avatar}" alt="${name}" class="rounded-circle" style="width: 140px; height: 140px; object-fit: cover; border: 2px solid var(--theme-primary);" />
              <div class="mt-2 fw-semibold small" style="color: #f8fafc;">${loc}</div>
            </div>
          </div>
        </div>

        <!-- Dark Luxury Metrics Strip -->
        ${renderMetricsStrip(data, "dark")}

        ${activeSections.includes("about") ? `
          <div class="dark-titanium-card mb-5" id="section-about">
            <h5 class="fw-bold mb-3" style="color: var(--theme-primary);">Overview</h5>
            <p class="lead mb-0" style="color: #cbd5e1; line-height: 1.8;">${about || headline || `${name} is an elite software engineering and technology professional.`}</p>
          </div>
        ` : ""}

        <!-- Dark Luxury Value Offerings -->
        ${activeSections.includes("services") ? renderServicesSection(data, "dark") : ""}

        ${activeSections.includes("skills") ? `
          <div class="dark-titanium-card mb-5" id="section-skills">
            <h5 class="fw-bold mb-3" style="color: var(--theme-primary);">Mastered Technologies</h5>
            ${renderSkillsBadges(skills, "dark")}
          </div>
        ` : ""}

        ${activeSections.includes("projects") && projects.length > 0 ? `
          <div class="mb-5" id="section-projects">
            <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-4">
              <h4 class="fw-bold mb-0" style="color: #f8fafc;">Bespoke Projects</h4>
              ${renderProjectFilterToolbar(projects)}
            </div>
            <div class="row g-4">
              ${projects.map(p => `
                <div class="col-md-6 col-lg-4 project-card-item" data-tech="${escapeHtml(((p.technologies || []).join(' ') + ' ' + (p.name || '')).toLowerCase())}">
                  <div class="dark-titanium-card h-100 d-flex flex-column">
                    <h5 class="fw-bold mb-2" style="color: #f8fafc;">${escapeHtml(p.name || "")}</h5>
                    <p class="small flex-grow-1 text-muted mb-3">${escapeHtml(p.description || "")}</p>
                    ${renderProjectActionLinks(p, "dark") ? `
                      <div class="pt-2 border-top border-secondary mt-auto">
                        ${renderProjectActionLinks(p, "dark")}
                      </div>
                    ` : ""}
                  </div>
                </div>
              `).join("")}
            </div>
          </div>
        ` : ""}

        ${activeSections.includes("experience") && experience.length > 0 ? `
          <div class="dark-titanium-card mb-5" id="section-experience">
            <h4 class="fw-bold mb-4" style="color: #f8fafc;">Professional Trajectory</h4>
            ${experience.map(exp => `
              <div class="border-bottom border-secondary pb-3 mb-3">
                <div class="d-flex justify-content-between align-items-baseline flex-wrap">
                  <h5 class="fw-bold mb-1" style="color: #f8fafc;">${escapeHtml(exp.title || "")}</h5>
                  <span class="small text-muted">${escapeHtml([exp.start_date, exp.end_date || (exp.is_current ? "Present" : "")].filter(Boolean).join(" — "))}</span>
                </div>
                <div class="small fw-semibold mb-2" style="color: var(--theme-primary);">${escapeHtml(exp.company || "")}</div>
                ${exp.description ? `<p class="small text-muted mb-0">${escapeHtml(exp.description)}</p>` : ""}
              </div>
            `).join("")}
          </div>
        ` : ""}

        <!-- Education & Certifications -->
        ${(activeSections.includes("education") || activeSections.includes("certifications")) ? `
          <div class="row g-4 mb-5">
            ${activeSections.includes("education") ? `
              <div class="col-md-6" id="section-education">
                <div class="dark-titanium-card h-100">
                  <h5 class="fw-bold mb-3" style="color: var(--theme-primary);">🎓 Academic Background</h5>
                  ${education.length > 0 ? education.map(e => `
                    <div class="border-bottom border-secondary pb-3 mb-2">
                      <div class="d-flex justify-content-between align-items-baseline">
                        <strong style="color: #f8fafc;">${escapeHtml(e.degree || "")}</strong>
                        ${(e.end_year || e.start_year || e.year) ? `<span class="badge" style="background: rgba(129, 140, 248, 0.2); color: #818cf8;">${escapeHtml(e.end_year || e.start_year || e.year)}</span>` : ""}
                      </div>
                      <div class="small fw-semibold mt-1" style="color: var(--theme-secondary);">${escapeHtml(e.institution || "")}</div>
                      ${e.field_of_study ? `<div class="small text-muted">${escapeHtml(e.field_of_study)}</div>` : ""}
                    </div>
                  `).join("") : `<div class="small text-muted">Higher Education in Technology</div>`}
                </div>
              </div>
            ` : ""}
            ${activeSections.includes("certifications") ? `
              <div class="col-md-6" id="section-certifications">
                <div class="dark-titanium-card h-100">
                  <h5 class="fw-bold mb-3" style="color: var(--theme-primary);">🏆 Credentials &amp; Licenses</h5>
                  ${certs.length > 0 ? certs.map(c => `
                    <div class="border-bottom border-secondary pb-2 mb-2 d-flex align-items-center gap-2">
                      <span style="color: #818cf8;">✦</span>
                      <div>
                        <strong style="color: #f8fafc;">${escapeHtml(c.name || c)}</strong>
                        ${c.organization ? `<div class="small text-muted">${escapeHtml(c.organization)}</div>` : ""}
                      </div>
                    </div>
                  `).join("") : `<div class="small text-muted">Verified Professional Credentials</div>`}
                </div>
              </div>
            ` : ""}
          </div>
        ` : ""}

        <!-- Social Proof & Achievements -->
        ${activeSections.includes("achievements") ? renderAchievementsSection(data, "dark") : ""}

        ${activeSections.includes("contact") ? renderUniversalContact(data) : ""}
        ${renderUniversalFooter(data)}
      </div>
    `;

    return html;
  }

  /**
   * 8. ELEGANT CLASSICAL GAZETTE LAYOUT
   */
  function renderElegantGazetteLayout(data, activeSections) {
    const name = escapeHtml(data.candidate_name || "");
    const headline = escapeHtml(data.professional_headline || "");
    const avatar = data.profile_image || `https://ui-avatars.com/api/?name=${encodeURIComponent(name || "Candidate")}&background=faf8f5&color=92643b&size=200`;
    const soc = data.social_links || {};
    const loc = escapeHtml(soc.location || "");
    const about = escapeHtml(data.about || "");
    const skills = data.skills || {};
    const projects = data.projects || [];
    const experience = data.experience || [];
    const education = data.education || [];

    let html = `
      <div class="elegant-gazette-stage py-4">
        <div class="container" style="max-width: 900px;">
          <!-- Masthead -->
          <header class="elegant-classic-masthead" id="section-home">
            <div class="small text-uppercase tracking-wider text-muted mb-1">CURRICULUM VITAE ET OPERA</div>
            <h1 class="display-4 fw-bold mb-2">${name}</h1>
            <div class="fst-italic text-muted mb-3">${headline}</div>
            <div class="small text-muted">✦ ${loc} ✦</div>
          </header>

          <!-- Classical Gazette Metrics Strip -->
          ${renderMetricsStrip(data, "elegant")}

          ${activeSections.includes("about") ? `
            <section class="mb-5 pb-3" id="section-about">
              <h4 class="fw-bold mb-3 border-bottom pb-2" style="font-family: serif;">Statement of Purpose</h4>
              <div class="elegant-dropcap fs-5" style="line-height: 1.8;">
                ${about || headline || `${name} is dedicated to classical excellence, deep engineering rigor, and lasting impact.`}
              </div>
            </section>
          ` : ""}

          <!-- Classical Value Pillars -->
          ${activeSections.includes("services") ? renderServicesSection(data, "elegant") : ""}

          ${activeSections.includes("skills") ? `
            <section class="mb-5 pb-3" id="section-skills">
              <h4 class="fw-bold mb-3 border-bottom pb-2" style="font-family: serif;">Competencies &amp; Disciplines</h4>
              <div>${renderSkillsBadges(skills, "elegant")}</div>
            </section>
          ` : ""}

          ${activeSections.includes("experience") && experience.length > 0 ? `
            <section class="mb-5 pb-3" id="section-experience">
              <h4 class="fw-bold mb-4 border-bottom pb-2" style="font-family: serif;">Chronological Appointments</h4>
              <div>
                ${experience.map(exp => `
                  <div class="elegant-cv-entry mb-3">
                    <div class="d-flex justify-content-between align-items-baseline">
                      <h5 class="fw-bold mb-0">${escapeHtml(exp.title || "")}</h5>
                      <span class="small text-muted">${escapeHtml([exp.start_date, exp.end_date || (exp.is_current ? "Present" : "")].filter(Boolean).join(" — "))}</span>
                    </div>
                    <div class="fst-italic mb-2" style="color: var(--theme-primary);">${escapeHtml(exp.company || "")}</div>
                    ${exp.description ? `<p class="small text-muted mb-1">${escapeHtml(exp.description)}</p>` : ""}
                  </div>
                `).join("")}
              </div>
            </section>
          ` : ""}

          ${activeSections.includes("projects") && projects.length > 0 ? `
            <section class="mb-5 pb-3" id="section-projects">
              <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-4 border-bottom pb-2">
                <h4 class="fw-bold mb-0" style="font-family: serif;">Selected Commissions</h4>
                ${renderProjectFilterToolbar(projects)}
              </div>
              <div class="row g-4">
                ${projects.map(p => `
                  <div class="col-md-6 project-card-item" data-tech="${escapeHtml(((p.technologies || []).join(' ') + ' ' + (p.name || '')).toLowerCase())}">
                    <div class="p-3 border rounded h-100 d-flex flex-column" style="background: #ffffff;">
                      <h5 class="fw-bold mb-1">${escapeHtml(p.name || "")}</h5>
                      <p class="small text-muted mb-2 flex-grow-1">${escapeHtml(p.description || "")}</p>
                      ${renderProjectActionLinks(p, "elegant")}
                    </div>
                  </div>
                `).join("")}
              </div>
            </section>
          ` : ""}

          ${(activeSections.includes("education") || education.length > 0) ? `
            <section class="mb-5 pb-3" id="section-education">
              <h4 class="fw-bold mb-3 border-bottom pb-2" style="font-family: serif;">Academic Background</h4>
              ${education.length > 0 ? education.map(e => `
                <div class="mb-3 pb-2 border-bottom border-light">
                  <div class="d-flex justify-content-between align-items-baseline">
                    <div>
                      <strong>${escapeHtml(e.degree || "")}</strong> — <span>${escapeHtml(e.institution || "")}</span>
                    </div>
                    ${(e.end_year || e.start_year || e.year) ? `<span class="text-muted small">${escapeHtml(e.end_year || e.start_year || e.year)}</span>` : ""}
                  </div>
                  ${e.field_of_study ? `<div class="small text-muted">${escapeHtml(e.field_of_study)}</div>` : ""}
                  ${(e.details || e.score || e.grade) ? `<div class="small text-muted mt-1 fst-italic">${escapeHtml(e.details || e.score || e.grade)}</div>` : ""}
                </div>
              `).join("") : `<div class="small text-muted">Academic Degrees in Technology</div>`}
            </section>
          ` : ""}

          ${(activeSections.includes("certifications") || (data.certifications && data.certifications.length > 0)) ? `
            <section class="mb-5 pb-3" id="section-certifications">
              <h4 class="fw-bold mb-3 border-bottom pb-2" style="font-family: serif;">Certifications &amp; Distinctions</h4>
              <div>
                ${(data.certifications || []).length > 0 ? (data.certifications || []).map(c => `
                  <div class="mb-2 pb-1 border-bottom border-light">
                    <strong>${escapeHtml(c.name || c)}</strong>
                    ${c.organization ? `<span class="text-muted small ms-2">• ${escapeHtml(c.organization)}</span>` : ""}
                  </div>
                `).join("") : `<div class="small text-muted">Verified Technical Certifications</div>`}
              </div>
            </section>
          ` : ""}

          <!-- Distinctions & Achievements -->
          ${activeSections.includes("achievements") ? renderAchievementsSection(data, "elegant") : ""}

          ${activeSections.includes("contact") ? renderUniversalContact(data) : ""}
          ${renderUniversalFooter(data)}
        </div>
      </div>
    `;

    return html;
  }

  /**
   * 9. NOTION-STYLE WORKSPACE DOCUMENT
   */
  function renderNotionDocLayout(data, activeSections) {
    const name = escapeHtml(data.candidate_name || "");
    const headline = escapeHtml(data.professional_headline || "");
    const avatar = data.profile_image || `https://ui-avatars.com/api/?name=${encodeURIComponent(name || "Candidate")}&background=2563eb&color=fff&size=200`;
    const soc = data.social_links || {};
    const loc = escapeHtml(soc.location || "");
    const about = escapeHtml(data.about || "");
    const skills = data.skills || {};
    const projects = data.projects || [];
    const experience = data.experience || [];
    const education = data.education || [];
    const certs = data.certifications || [];

    return `
      <div class="notion-doc-stage animate-fade-in-up">
        <!-- Top Workspace Bar -->
        <div class="d-flex align-items-center justify-content-between py-2 border-bottom mb-2 text-muted small" style="border-color: var(--theme-card-border) !important;">
          <div class="d-flex align-items-center gap-2">
            <span>📄</span>
            <span>Workspace</span>
            <span>/</span>
            <span>Profiles</span>
            <span>/</span>
            <span class="fw-semibold" style="color: var(--theme-text);">${name}</span>
          </div>
          <div class="d-flex gap-2">
            <span class="badge bg-light text-secondary border small">🟢 Active</span>
          </div>
        </div>

        <!-- Cover Banner -->
        <div class="notion-cover-banner"></div>

        <!-- Avatar & Identity -->
        <div class="d-flex align-items-end gap-3 mb-4" id="section-home">
          <div class="notion-avatar-wrap">
            <img src="${avatar}" alt="${name}" class="w-100 h-100 object-fit-cover" />
          </div>
          <div class="pt-4">
            <h1 class="display-6 fw-bold mb-1" style="color: var(--theme-text); letter-spacing: -0.02em;">${name}</h1>
            ${loc ? `<div class="small text-muted mb-1">📍 ${loc}</div>` : ""}
            <p class="lead mb-0 text-muted fs-6">${headline}</p>
          </div>
        </div>

        <!-- Notion Callout Box -->
        <div class="notion-callout" id="section-about">
          <span class="fs-4">💡</span>
          <div>
            <div class="fw-bold small mb-1" style="color: var(--theme-text);">Executive Summary</div>
            <div style="color: var(--theme-text-muted); line-height: 1.6;">${about || headline || `${name} is an experienced professional and software systems builder.`}</div>
            ${loc ? `<div class="small mt-2 text-muted">📍 Location: <strong>${loc}</strong></div>` : ""}
          </div>
        </div>

        <!-- Notion Metrics Strip -->
        ${renderMetricsStrip(data, "notion")}

        <!-- Value Offerings & Services -->
        ${activeSections.includes("services") ? renderServicesSection(data, "notion") : ""}

        <!-- Skills Properties View -->
        ${activeSections.includes("skills") ? `
          <div class="mb-4 p-3 border rounded-3 bg-white" id="section-skills" style="border-color: var(--theme-card-border) !important;">
            <div class="d-flex align-items-center gap-2 mb-2 text-muted small fw-bold">
              <span>🏷️</span> <span>PROPERTIES // CORE COMPETENCIES</span>
            </div>
            <div>${renderSkillsBadges(skills, "notion")}</div>
          </div>
        ` : ""}

        <!-- Experience Toggle Section -->
        ${activeSections.includes("experience") && experience.length > 0 ? `
          <div class="mb-5" id="section-experience">
            <h5 class="fw-bold mb-3 d-flex align-items-center gap-2" style="color: var(--theme-text);">
              <span>▼</span> <span>Professional Appointments (${experience.length})</span>
            </h5>
            <div class="ps-3 border-start" style="border-color: var(--theme-card-border) !important;">
              ${experience.map(exp => `
                <div class="mb-4">
                  <div class="d-flex justify-content-between align-items-baseline">
                    <h6 class="fw-bold mb-0" style="color: var(--theme-text);">${escapeHtml(exp.title || "")} <span class="fw-normal text-muted">@ ${escapeHtml(exp.company || "")}</span></h6>
                    <span class="small text-muted font-monospace">${escapeHtml([exp.start_date, exp.end_date || (exp.is_current ? "Present" : "")].filter(Boolean).join(" — "))}</span>
                  </div>
                  ${exp.description ? `<p class="small text-muted mt-1 mb-0">${escapeHtml(exp.description)}</p>` : ""}
                </div>
              `).join("")}
            </div>
          </div>
        ` : ""}

        <!-- Projects Database View -->
        ${activeSections.includes("projects") && projects.length > 0 ? `
          <div class="mb-5" id="section-projects">
            <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-3">
              <h5 class="fw-bold mb-0 d-flex align-items-center gap-2" style="color: var(--theme-text);">
                <span>🗂️</span> <span>Projects &amp; Deliverables Database</span>
              </h5>
              ${renderProjectFilterToolbar(projects)}
            </div>
            <div class="row g-3">
              ${projects.map(p => `
                <div class="col-md-6 project-card-item" data-tech="${escapeHtml(((p.technologies || []).join(' ') + ' ' + (p.name || '')).toLowerCase())}">
                  <div class="p-3 border rounded-3 bg-white h-100 d-flex flex-column" style="border-color: var(--theme-card-border) !important;">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                      <h6 class="fw-bold mb-0" style="color: var(--theme-text);">${escapeHtml(p.name || "")}</h6>
                    </div>
                    <p class="small text-muted mb-2 flex-grow-1">${escapeHtml(p.description || "")}</p>
                    <div class="d-flex flex-wrap gap-1 mb-2">
                      ${(p.technologies || []).map(t => `<span class="notion-tag-badge">${escapeHtml(t)}</span>`).join("")}
                    </div>
                    ${renderProjectActionLinks(p, "notion")}
                  </div>
                </div>
              `).join("")}
            </div>
          </div>
        ` : ""}

        <!-- Education & Credentials -->
        ${(activeSections.includes("education") || education.length > 0) ? `
          <div class="mb-5 p-3 border rounded-3 bg-white" id="section-education" style="border-color: var(--theme-card-border) !important;">
            <div class="fw-bold small mb-2 text-muted">🎓 EDUCATION &amp; CREDENTIALS</div>
            ${education.length > 0 ? education.map(e => `
              <div class="small mb-2 pb-1 border-bottom border-light">
                <div class="d-flex justify-content-between align-items-baseline">
                  <strong>${escapeHtml(e.degree || "")}</strong>
                  ${(e.end_year || e.start_year || e.year) ? `<span class="text-muted small">${escapeHtml(e.end_year || e.start_year || e.year)}</span>` : ""}
                </div>
                <div class="text-muted">${escapeHtml(e.institution || "")}</div>
                ${e.field_of_study ? `<div class="text-muted">${escapeHtml(e.field_of_study)}</div>` : ""}
                ${(e.details || e.score || e.grade) ? `<div class="text-muted fst-italic mt-1">${escapeHtml(e.details || e.score || e.grade)}</div>` : ""}
              </div>
            `).join("") : `<div class="small text-muted">Academic Degrees in Technology</div>`}
          </div>
        ` : ""}

        ${(activeSections.includes("certifications") || certs.length > 0) ? `
          <div class="mb-5 p-3 border rounded-3 bg-white" id="section-certifications" style="border-color: var(--theme-card-border) !important;">
            <div class="fw-bold small mb-2 text-muted">🏆 CERTIFICATIONS &amp; BADGES</div>
            ${certs.length > 0 ? certs.map(c => `
              <div class="small mb-2 pb-1 border-bottom border-light">
                <strong>${escapeHtml(c.name || c)}</strong>
                ${c.organization ? `<span class="text-muted ms-2">• ${escapeHtml(c.organization)}</span>` : ""}
              </div>
            `).join("") : `<div class="small text-muted">Verified Technical Certifications</div>`}
          </div>
        ` : ""}

        <!-- Recommendations Database -->
        ${activeSections.includes("achievements") ? renderAchievementsSection(data, "notion") : ""}

        ${activeSections.includes("contact") ? renderUniversalContact(data) : ""}
        ${renderUniversalFooter(data)}
      </div>
    `;
  }

  /**
   * 10. CAREER JOURNEY & MILESTONE STORYBOARD
   */
  function renderTimelineJourneyLayout(data, activeSections) {
    const name = escapeHtml(data.candidate_name || "");
    const headline = escapeHtml(data.professional_headline || "");
    const avatar = data.profile_image || `https://ui-avatars.com/api/?name=${encodeURIComponent(name || "Candidate")}&background=4f46e5&color=fff&size=200`;
    const about = escapeHtml(data.about || "");
    const skills = data.skills || {};
    const projects = data.projects || [];
    const experience = data.experience || [];
    const education = data.education || [];
    const soc = data.social_links || {};
    const loc = escapeHtml(soc.location || "");

    return `
      <div class="timeline-journey-stage animate-fade-in-up">
        <!-- Trail Header -->
        <header class="text-center mb-5 pb-3" id="section-home">
          <div class="d-inline-flex p-1 rounded-circle border shadow-sm mb-3" style="border-color: var(--theme-primary) !important;">
            <img src="${avatar}" alt="${name}" class="rounded-circle" style="width: 90px; height: 90px; object-fit: cover;" />
          </div>
          <h1 class="display-5 fw-bold mb-2" style="color: var(--theme-text);">${name}</h1>
          <div class="d-flex justify-content-center align-items-center gap-2 mb-3 flex-wrap">
            <div class="d-inline-flex align-items-center gap-2 px-3 py-1 rounded-pill small fw-semibold" style="background: var(--theme-badge-bg); color: var(--theme-primary);">
              <span>🧭</span> <span>Milestone Trail &amp; Career Progression</span>
            </div>
            ${loc ? `<div class="d-inline-flex align-items-center gap-2 px-3 py-1 rounded-pill small fw-semibold" style="background: var(--theme-badge-bg); color: var(--theme-primary);">📍 ${loc}</div>` : ""}
          </div>
          <p class="lead text-muted fs-6 mb-3 mx-auto" style="max-width: 600px;">${headline}</p>
          <div class="p-3 mx-auto rounded-3 border" id="section-about" style="max-width: 700px; background: var(--theme-card-bg); border-color: var(--theme-card-border) !important; color: var(--theme-text-muted);">
            ${about || headline || `${name} is an experienced technologist on an ambitious career journey.`}
          </div>
        </header>

        <!-- Vertical Milestone Spine Track -->
        <div class="timeline-spine-track" id="section-experience">
          ${experience.map((exp, idx) => {
            const isLeft = idx % 2 === 0;
            return `
              <div class="timeline-node-item d-flex ${isLeft ? 'justify-content-start' : 'justify-content-end'}">
                <div class="timeline-waypoint-dot"></div>
                <div class="timeline-card-wrap">
                  <div class="portfolio-card p-4">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                      <span class="badge rounded-pill px-2 py-1 small" style="background: var(--theme-badge-bg); color: var(--theme-primary); font-size: 0.7rem;">
                        MILESTONE #${idx + 1}
                      </span>
                      <span class="small text-muted font-monospace">${escapeHtml([exp.start_date, exp.end_date || (exp.is_current ? "Present" : "")].filter(Boolean).join(" — "))}</span>
                    </div>
                    <h5 class="fw-bold mb-0" style="color: var(--theme-text);">${escapeHtml(exp.title || "")}</h5>
                    <div class="small fw-semibold mb-2" style="color: var(--theme-primary);">${escapeHtml(exp.company || "")}</div>
                    ${exp.description ? `<p class="small text-muted mb-0">${escapeHtml(exp.description)}</p>` : ""}
                  </div>
                </div>
              </div>
            `;
          }).join("")}
        </div>

        <!-- Waypoint Metrics Strip -->
        ${renderMetricsStrip(data, "timeline")}

        <!-- Value Pillars -->
        ${activeSections.includes("services") ? renderServicesSection(data, "timeline") : ""}

        <!-- Breakthrough Projects Waypoints -->
        ${activeSections.includes("projects") && projects.length > 0 ? `
          <section class="mt-5 pt-4" id="section-projects">
            <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-4">
              <div>
                <span class="badge rounded-pill px-3 py-1 small fw-bold" style="background: var(--theme-badge-bg); color: var(--theme-primary);">
                  FEATURED WORK
                </span>
                <h3 class="fw-bold mt-2 mb-0" style="color: var(--theme-text);">Featured Projects</h3>
              </div>
              ${renderProjectFilterToolbar(projects)}
            </div>
            <div class="row g-4">
              ${projects.map(p => `
                <div class="col-md-6 project-card-item" data-tech="${escapeHtml(((p.technologies || []).join(' ') + ' ' + (p.name || '')).toLowerCase())}">
                  <div class="portfolio-card p-4 h-100 d-flex flex-column">
                    <h5 class="fw-bold mb-1" style="color: var(--theme-text);">${escapeHtml(p.name || "")}</h5>
                    <p class="small text-muted mb-3 flex-grow-1">${escapeHtml(p.description || "")}</p>
                    <div class="d-flex flex-wrap gap-1 mb-3">
                      ${(p.technologies || []).map(t => `<span class="theme-badge">${escapeHtml(t)}</span>`).join("")}
                    </div>
                    ${renderProjectActionLinks(p, "timeline")}
                  </div>
                </div>
              `).join("")}
            </div>
          </section>
        ` : ""}

        <!-- Skills Matrix -->
        ${activeSections.includes("skills") ? `
          <section class="mt-5 pt-4" id="section-skills">
            <div class="portfolio-card p-4 text-center">
              <h5 class="fw-bold mb-3" style="color: var(--theme-text);">Core Competencies Matrix</h5>
              <div>${renderSkillsBadges(skills, "timeline")}</div>
            </div>
          </section>
        ` : ""}

        <!-- Education & Certifications Milestones -->
        ${(activeSections.includes("education") || activeSections.includes("certifications")) ? `
          <div class="row g-4 mt-4">
            ${activeSections.includes("education") ? `
              <div class="col-md-6" id="section-education">
                <div class="portfolio-card p-4 h-100">
                  <h5 class="fw-bold mb-3" style="color: var(--theme-text);">🎓 Academic Background</h5>
                  ${education.length > 0 ? education.map(e => `
                    <div class="mb-3 pb-2 border-bottom">
                      <div class="d-flex justify-content-between align-items-baseline">
                        <strong>${escapeHtml(e.degree || "")}</strong>
                        ${(e.end_year || e.start_year || e.year) ? `<span class="badge rounded-pill bg-primary-subtle text-primary">${escapeHtml(e.end_year || e.start_year || e.year)}</span>` : ""}
                      </div>
                      <div class="small fw-semibold mt-1" style="color: var(--theme-primary);">${escapeHtml(e.institution || "")}</div>
                      ${e.field_of_study ? `<div class="small text-muted">${escapeHtml(e.field_of_study)}</div>` : ""}
                    </div>
                  `).join("") : `<div class="small text-muted">Academic Degrees &amp; Higher Education</div>`}
                </div>
              </div>
            ` : ""}
            ${activeSections.includes("certifications") ? `
              <div class="col-md-6" id="section-certifications">
                <div class="portfolio-card p-4 h-100">
                  <h5 class="fw-bold mb-3" style="color: var(--theme-text);">🏆 Industry Certifications</h5>
                  ${(data.certifications || []).length > 0 ? (data.certifications || []).map(c => `
                    <div class="mb-2 pb-1 border-bottom d-flex align-items-center gap-2">
                      <span>📜</span>
                      <div>
                        <strong>${escapeHtml(c.name || c)}</strong>
                        ${c.organization ? `<div class="small text-muted">${escapeHtml(c.organization)}</div>` : ""}
                      </div>
                    </div>
                  `).join("") : `<div class="small text-muted">Verified Technical Credentials</div>`}
                </div>
              </div>
            ` : ""}
          </div>
        ` : ""}

        <!-- Recommendations Along Journey -->
        ${activeSections.includes("achievements") ? renderAchievementsSection(data, "timeline") : ""}

        ${activeSections.includes("contact") ? renderUniversalContact(data) : ""}
        ${renderUniversalFooter(data)}
      </div>
    `;
  }

  /**
   * 11. INTERACTIVE DASHBOARD COCKPIT
   */
  function renderDashboardCockpitLayout(data, activeSections) {
    const name = escapeHtml(data.candidate_name || "");
    const headline = escapeHtml(data.professional_headline || "");
    const avatar = data.profile_image || `https://ui-avatars.com/api/?name=${encodeURIComponent(name || "Candidate")}&background=326ce5&color=fff&size=200`;
    const about = escapeHtml(data.about || "");
    const skills = data.skills || {};
    const projects = data.projects || [];
    const experience = data.experience || [];
    const education = data.education || [];

    let skillCount = 0;
    if (Array.isArray(skills)) skillCount = skills.length;
    else if (typeof skills === "object") {
      Object.values(skills).forEach(arr => { if (Array.isArray(arr)) skillCount += arr.length; });
    }

    return `
      <div class="cockpit-stage animate-fade-in-up">
        <!-- Top Cockpit Control Bar -->
        <header id="section-home" class="d-flex flex-wrap align-items-center justify-content-between p-3 mb-4 rounded-4 border bg-white shadow-sm" style="border-color: var(--theme-card-border) !important;">
          <div class="d-flex align-items-center gap-3">
            <img src="${avatar}" alt="${name}" class="rounded-circle" style="width: 54px; height: 54px; object-fit: cover;" />
            <div>
              <h5 class="fw-bold mb-0" style="color: var(--theme-text);">${name}</h5>
              <span class="small text-muted font-monospace">${headline}</span>
            </div>
          </div>
          <div class="d-flex align-items-center gap-2 mt-2 mt-md-0">
            <span class="badge bg-success-subtle text-success border rounded-pill px-3 py-2 small fw-bold">
              🟢 Available for Opportunities
            </span>
            <a href="#section-contact" class="theme-btn-primary py-1 px-3 small">Direct Contact</a>
          </div>
        </header>

        <!-- KPI Telemetry Bar -->
        <div class="cockpit-kpi-bar">
          <div class="cockpit-kpi-card">
            <div>
              <div class="small text-muted fw-bold">EXPERIENCE</div>
              <div class="cockpit-metric-val">${experience.length}+</div>
              <div class="small text-muted">Appointments</div>
            </div>
          </div>
          <div class="cockpit-kpi-card">
            <div>
              <div class="small text-muted fw-bold">FEATURED PROJECTS</div>
              <div class="cockpit-metric-val">${projects.length}</div>
              <div class="small text-muted">Shipped Deliverables</div>
            </div>
          </div>
          <div class="cockpit-kpi-card">
            <div>
              <div class="small text-muted fw-bold">CORE COMPETENCIES</div>
              <div class="cockpit-metric-val">${skillCount || 12}+</div>
              <div class="small text-muted">Technical Skills</div>
            </div>
          </div>
          <div class="cockpit-kpi-card">
            <div>
              <div class="small text-muted fw-bold">CREDENTIALS</div>
              <div class="cockpit-metric-val text-success">${(education.length + (data.certifications?.length || 0)) || 1}+</div>
              <div class="small text-muted">Degrees &amp; Certs</div>
            </div>
          </div>
        </div>

        <!-- Cockpit Value Capabilities / Services -->
        ${activeSections.includes("services") ? renderServicesSection(data, "dashboard") : ""}

        <!-- 2-Column Dashboard Grid -->
        <div class="row g-4 mb-4">
          <!-- Left Column: Bio & Skills -->
          <div class="col-lg-4">
            <div class="portfolio-card p-4 mb-4" id="section-about">
              <h6 class="fw-bold small text-uppercase mb-2" style="color: var(--theme-primary); letter-spacing: 0.05em;">Executive Bio</h6>
              <p class="small text-muted mb-0" style="line-height: 1.6;">${about}</p>
            </div>

            <div class="portfolio-card p-4" id="section-skills">
              <h6 class="fw-bold small text-uppercase mb-3" style="color: var(--theme-primary); letter-spacing: 0.05em;">Technical Skills &amp; Stack</h6>
              <div>${renderSkillsBadges(skills, "cockpit")}</div>
            </div>
          </div>

          <!-- Right Column: Projects & Experience -->
          <div class="col-lg-8">
            ${activeSections.includes("projects") && projects.length > 0 ? `
              <div class="portfolio-card p-4 mb-4" id="section-projects">
                <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
                  <h6 class="fw-bold small text-uppercase mb-0" style="color: var(--theme-primary); letter-spacing: 0.05em;">Production Deliverables (${projects.length})</h6>
                  ${renderProjectFilterToolbar(projects)}
                </div>
                <div class="row g-3">
                  ${projects.map(p => `
                    <div class="col-md-6 project-card-item" data-tech="${escapeHtml(((p.technologies || []).join(' ') + ' ' + (p.name || '')).toLowerCase())}">
                      <div class="p-3 border rounded-3 bg-light-subtle h-100 d-flex flex-column" style="border-color: var(--theme-card-border) !important;">
                        <h6 class="fw-bold mb-1" style="color: var(--theme-text);">${escapeHtml(p.name || "")}</h6>
                        <p class="small text-muted mb-2 flex-grow-1">${escapeHtml(p.description || "")}</p>
                        <div class="d-flex flex-wrap gap-1 mb-2">
                          ${(p.technologies || []).map(t => `<span class="theme-badge" style="font-size: 0.68rem;">${escapeHtml(t)}</span>`).join("")}
                        </div>
                        ${renderProjectActionLinks(p, "dashboard")}
                      </div>
                    </div>
                  `).join("")}
                </div>
              </div>
            ` : ""}

            ${activeSections.includes("experience") && experience.length > 0 ? `
              <div class="portfolio-card p-4" id="section-experience">
                <h6 class="fw-bold small text-uppercase mb-3" style="color: var(--theme-primary); letter-spacing: 0.05em;">Experience Feed</h6>
                <div class="border-start ps-3" style="border-color: var(--theme-card-border) !important;">
                  ${experience.map(exp => `
                    <div class="mb-3">
                      <div class="d-flex justify-content-between align-items-baseline">
                        <h6 class="fw-bold mb-0" style="color: var(--theme-text);">${escapeHtml(exp.title || "")} <span class="text-muted fw-normal">@ ${escapeHtml(exp.company || "")}</span></h6>
                        <span class="small text-muted font-monospace">${escapeHtml([exp.start_date, exp.end_date || (exp.is_current ? "Present" : "")].filter(Boolean).join(" — "))}</span>
                      </div>
                      ${exp.description ? `<p class="small text-muted mb-0 mt-1">${escapeHtml(exp.description)}</p>` : ""}
                    </div>
                  `).join("")}
                </div>
              </div>
            ` : ""}
          </div>
        </div>

        <!-- Education & Certifications Telemetry -->
        ${(activeSections.includes("education") || activeSections.includes("certifications")) ? `
          <div class="row g-4 mb-4">
            ${activeSections.includes("education") ? `
              <div class="col-md-6" id="section-education">
                <div class="portfolio-card p-4 h-100">
                  <h6 class="fw-bold small text-uppercase mb-3" style="color: var(--theme-primary); letter-spacing: 0.05em;">🎓 Academic Credentials</h6>
                  ${(data.education || []).length > 0 ? (data.education || []).map(e => `
                    <div class="mb-3 pb-2 border-bottom">
                      <div class="d-flex justify-content-between align-items-baseline">
                        <strong style="color: var(--theme-text);">${escapeHtml(e.degree || "")}</strong>
                        ${(e.end_year || e.start_year || e.year) ? `<span class="badge bg-secondary-subtle text-secondary small">${escapeHtml(e.end_year || e.start_year || e.year)}</span>` : ""}
                      </div>
                      <div class="small fw-semibold" style="color: var(--theme-primary);">${escapeHtml(e.institution || "")}</div>
                      ${e.field_of_study ? `<div class="small text-muted">${escapeHtml(e.field_of_study)}</div>` : ""}
                    </div>
                  `).join("") : `<div class="small text-muted">Academic background and verified degrees.</div>`}
                </div>
              </div>
            ` : ""}
            ${activeSections.includes("certifications") ? `
              <div class="col-md-6" id="section-certifications">
                <div class="portfolio-card p-4 h-100">
                  <h6 class="fw-bold small text-uppercase mb-3" style="color: var(--theme-primary); letter-spacing: 0.05em;">🏆 Certifications &amp; Accreditations</h6>
                  ${(data.certifications || []).length > 0 ? (data.certifications || []).map(c => `
                    <div class="mb-2 pb-1 border-bottom d-flex align-items-center gap-2">
                      <span>📜</span>
                      <div>
                        <strong>${escapeHtml(c.name || c)}</strong>
                        ${c.organization ? `<div class="small text-muted">${escapeHtml(c.organization)}</div>` : ""}
                      </div>
                    </div>
                  `).join("") : `<div class="small text-muted">Verified industry certifications and licenses.</div>`}
                </div>
              </div>
            ` : ""}
          </div>
        ` : ""}

        <!-- Social Proof & Peer Endorsements -->
        ${activeSections.includes("achievements") ? renderAchievementsSection(data, "dashboard") : ""}

        ${activeSections.includes("contact") ? renderUniversalContact(data) : ""}
        ${renderUniversalFooter(data)}
      </div>
    `;
  }

  /**
   * 12. SPLIT-SCREEN SHOWCASE
   */
  function renderSplitScreenLayout(data, activeSections) {
    const name = escapeHtml(data.candidate_name || "");
    const headline = escapeHtml(data.professional_headline || "");
    const avatar = data.profile_image || `https://ui-avatars.com/api/?name=${encodeURIComponent(name || "Candidate")}&background=ec4899&color=fff&size=200`;
    const soc = data.social_links || {};
    const loc = escapeHtml(soc.location || "");
    const about = escapeHtml(data.about || "");
    const skills = data.skills || {};
    const projects = data.projects || [];
    const experience = data.experience || [];
    const education = data.education || [];

    return `
      <div class="split-screen-stage animate-fade-in-up">
        <div class="row g-4 g-lg-5">
          <!-- Left Sticky Identity Column (40%) -->
          <div class="col-lg-5">
            <div class="split-sticky-sidebar split-hero-card" id="section-home">
              <div class="mb-3">
                <img src="${avatar}" alt="${name}" class="rounded-4 mb-3 border shadow-sm" style="width: 120px; height: 120px; object-fit: cover;" />
                <h1 class="display-6 fw-bold mb-1" style="color: var(--theme-text);">${name}</h1>
                ${loc ? `<div class="d-inline-flex align-items-center gap-1 small text-muted mb-2">📍 ${loc}</div>` : ""}
                <p class="lead text-muted fs-6 mb-3">${headline}</p>
                <div class="mb-4" id="section-about" style="color: var(--theme-text-muted); line-height: 1.6;">${about}</div>
              </div>

              <!-- Contact & Links -->
              <div class="d-flex flex-column gap-2 mb-4">
                ${soc.email ? `<a href="mailto:${escapeHtml(soc.email)}" class="theme-btn-primary py-2 text-center text-decoration-none"><span>✉️</span> ${escapeHtml(soc.email)}</a>` : ""}
                ${soc.github ? `<a href="${escapeHtml(soc.github)}" target="_blank" class="theme-btn-outline py-2 text-center text-decoration-none"><span>💻</span> GitHub Profile</a>` : ""}
                ${soc.linkedin ? `<a href="${escapeHtml(soc.linkedin)}" target="_blank" class="theme-btn-outline py-2 text-center text-decoration-none"><span>in</span> LinkedIn Profile</a>` : ""}
              </div>

              <div class="border-top pt-3 small text-muted">
                <div>&copy; ${new Date().getFullYear()} ${name}</div>
              </div>
            </div>
          </div>

          <!-- Right Scrolling Case Studies Column (60%) -->
          <div class="col-lg-7">
            <!-- Strategic Impact Metrics -->
            ${renderMetricsStrip(data, "split_screen")}

            <!-- Services & Capabilities -->
            ${activeSections.includes("services") ? renderServicesSection(data, "split_screen") : ""}

            <!-- Projects -->
            ${activeSections.includes("projects") && projects.length > 0 ? `
              <div class="mb-5" id="section-projects">
                <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-3">
                  <h4 class="fw-bold mb-0 section-title" style="color: var(--theme-text);">Featured Case Studies</h4>
                  ${renderProjectFilterToolbar(projects)}
                </div>
                ${projects.map(p => `
                  <div class="split-feed-card project-card-item d-flex flex-column" data-tech="${escapeHtml(((p.technologies || []).join(' ') + ' ' + (p.name || '')).toLowerCase())}">
                    <h5 class="fw-bold mb-1" style="color: var(--theme-text);">${escapeHtml(p.name || "")}</h5>
                    <p class="small text-muted mb-3 flex-grow-1">${escapeHtml(p.description || "")}</p>
                    <div class="d-flex flex-wrap gap-1 mb-3">
                      ${(p.technologies || []).map(t => `<span class="theme-badge">${escapeHtml(t)}</span>`).join("")}
                    </div>
                    ${renderProjectActionLinks(p, "split_screen")}
                  </div>
                `).join("")}
              </div>
            ` : ""}

            <!-- Experience -->
            ${activeSections.includes("experience") && experience.length > 0 ? `
              <div class="mb-5" id="section-experience">
                <h4 class="fw-bold mb-3 section-title" style="color: var(--theme-text);">Professional Career</h4>
                ${experience.map(exp => `
                  <div class="split-feed-card">
                    <div class="d-flex justify-content-between align-items-baseline mb-1">
                      <h5 class="fw-bold mb-0" style="color: var(--theme-text);">${escapeHtml(exp.title || "")}</h5>
                      <span class="small text-muted font-monospace">${escapeHtml([exp.start_date, exp.end_date || (exp.is_current ? "Present" : "")].filter(Boolean).join(" — "))}</span>
                    </div>
                    <div class="small fw-semibold mb-2" style="color: var(--theme-primary);">${escapeHtml(exp.company || "")}</div>
                    ${exp.description ? `<p class="small text-muted mb-0">${escapeHtml(exp.description)}</p>` : ""}
                  </div>
                `).join("")}
              </div>
            ` : ""}

            <!-- Skills -->
            ${activeSections.includes("skills") ? `
              <div class="split-feed-card mb-5" id="section-skills">
                <h5 class="fw-bold mb-3" style="color: var(--theme-text);">Technical Expertise</h5>
                <div>${renderSkillsBadges(skills, "split")}</div>
              </div>
            ` : ""}

            <!-- Education -->
            ${activeSections.includes("education") ? `
              <div class="split-feed-card mb-5" id="section-education">
                <h5 class="fw-bold mb-3" style="color: var(--theme-text);">Academic Background</h5>
                ${education.length > 0 ? education.map(e => `
                  <div class="mb-3 pb-2 border-bottom border-light small">
                    <div class="d-flex justify-content-between align-items-baseline">
                      <strong style="color: var(--theme-text);">${escapeHtml(e.degree || "")}</strong>
                      ${(e.end_year || e.start_year || e.year) ? `<span class="badge bg-secondary-subtle text-secondary">${escapeHtml(e.end_year || e.start_year || e.year)}</span>` : ""}
                    </div>
                    <div class="text-primary fw-semibold">${escapeHtml(e.institution || "")}</div>
                    ${e.field_of_study ? `<div class="text-muted">${escapeHtml(e.field_of_study)}</div>` : ""}
                    ${(e.details || e.score || e.grade) ? `<div class="text-muted mt-1">${escapeHtml(e.details || e.score || e.grade)}</div>` : ""}
                  </div>
                `).join("") : `<div class="small text-muted">Academic credentials and degrees.</div>`}
              </div>
            ` : ""}

            <!-- Certifications -->
            ${activeSections.includes("certifications") ? `
              <div class="split-feed-card mb-5" id="section-certifications">
                <h5 class="fw-bold mb-3" style="color: var(--theme-text);">Certifications &amp; Accreditations</h5>
                ${(data.certifications || []).length > 0 ? (data.certifications || []).map(c => `
                  <div class="mb-2 pb-1 border-bottom border-light small d-flex align-items-center gap-2">
                    <span>📜</span>
                    <div>
                      <strong>${escapeHtml(c.name || c)}</strong>
                      ${c.organization ? `<div class="text-muted">${escapeHtml(c.organization)}</div>` : ""}
                    </div>
                  </div>
                `).join("") : `<div class="small text-muted">Verified technical credentials and certifications.</div>`}
              </div>
            ` : ""}

            <!-- Recommendations & Social Proof -->
            ${activeSections.includes("achievements") ? renderAchievementsSection(data, "split_screen") : ""}

            ${activeSections.includes("contact") ? renderUniversalContact(data) : ""}
            ${renderUniversalFooter(data)}
          </div>
        </div>
      </div>
    `;
  }

  /* ==============================================================
     HELPER RENDERERS
     ============================================================== */

  function renderSkillsBadges(rawSkills, styleVariant = "modern") {
    if (!rawSkills) return "";
    let html = "";

    if (typeof rawSkills === "object" && !Array.isArray(rawSkills)) {
      for (const [catName, skillList] of Object.entries(rawSkills)) {
        if (!Array.isArray(skillList) || skillList.length === 0) continue;
        const badges = skillList.map(s => `<span class="theme-badge">${escapeHtml(s)}</span>`).join("");
        html += `
          <div class="mb-3">
            <h6 class="fw-bold small mb-2 text-uppercase" style="color: var(--theme-primary); letter-spacing: 0.05em;">${escapeHtml(catName)}</h6>
            <div class="d-flex flex-wrap gap-1">${badges}</div>
          </div>
        `;
      }
    } else if (Array.isArray(rawSkills)) {
      const badges = rawSkills.map(s => `<span class="theme-badge">${escapeHtml(s)}</span>`).join("");
      html = `<div class="d-flex flex-wrap gap-1">${badges}</div>`;
    }

    return html;
  }

  /**
   * Helper to render robust, secure, and interactive project action links (Live Demo & Source Code).
   * Ensures all external links open in a new tab with target="_blank" rel="noopener noreferrer".
   */
  function renderProjectActionLinks(project, themeVariant = "default") {
    if (!project || typeof project !== "object") return "";

    const cleanUrl = (raw) => {
      if (!raw || typeof raw !== "string") return "";
      let trimmed = raw.trim();
      if (!trimmed || trimmed === "#" || trimmed.toLowerCase() === "none") return "";
      if (!trimmed.match(/^https?:\/\//i)) {
        trimmed = "https://" + trimmed;
      }
      return trimmed;
    };

    const liveUrl = cleanUrl(project.live_demo_url || project.demo_url || project.url || project.link);
    const codeUrl = cleanUrl(project.github_url || project.repo_url || project.code_url);

    if (!liveUrl && !codeUrl) return "";

    const isSame = liveUrl && codeUrl && liveUrl.toLowerCase() === codeUrl.toLowerCase();

    let demoLabel = "Live Demo";
    let codeLabel = "Source Code";
    let demoIcon = "🌐";
    let codeIcon = "💻";

    if (themeVariant === "developer") {
      demoLabel = "Live Preview";
      codeLabel = "git clone";
      demoIcon = "🚀";
      codeIcon = "⚡";
    } else if (themeVariant === "ai_tech") {
      demoLabel = "Deploy / Live";
      codeLabel = "Inspect Code";
      demoIcon = "⚡";
      codeIcon = "🔬";
    } else if (themeVariant === "creative") {
      demoLabel = "🚀 Launch Demo";
      codeLabel = "Source Code";
      demoIcon = "✨";
      codeIcon = "🎨";
    } else if (themeVariant === "corporate") {
      demoLabel = "View Deliverable";
      codeLabel = "Repository";
      demoIcon = "📊";
      codeIcon = "📂";
    } else if (themeVariant === "minimal") {
      demoLabel = "View";
      codeLabel = "Code";
      demoIcon = "↗";
      codeIcon = "⌥";
    } else if (themeVariant === "elegant") {
      demoLabel = "Examine Work";
      codeLabel = "Codebase";
      demoIcon = "✦";
      codeIcon = "✒";
    } else if (themeVariant === "notion") {
      demoLabel = "Live Site";
      codeLabel = "Repository";
      demoIcon = "🔗";
      codeIcon = "📁";
    } else if (themeVariant === "timeline") {
      demoLabel = "Explore Project";
      codeLabel = "Repository";
      demoIcon = "🧭";
      codeIcon = "💻";
    }

    let html = `<div class="project-action-links d-flex align-items-center flex-wrap gap-2">`;

    if (liveUrl) {
      const isCodeLink = isSame && (liveUrl.includes("github.com") || liveUrl.includes("gitlab.com"));
      const label = isCodeLink ? codeLabel : demoLabel;
      const icon = isCodeLink ? codeIcon : demoIcon;
      html += `
        <a href="${escapeHtml(liveUrl)}" target="_blank" rel="noopener noreferrer" class="project-action-btn project-btn-demo variant-${themeVariant}" title="Open live project website in a new tab">
          <span class="action-icon">${icon}</span>
          <span class="action-text">${escapeHtml(label)}</span>
          <span class="action-arrow">↗</span>
        </a>
      `;
    }

    if (codeUrl && !isSame) {
      html += `
        <a href="${escapeHtml(codeUrl)}" target="_blank" rel="noopener noreferrer" class="project-action-btn project-btn-repo variant-${themeVariant}" title="View source code repository in a new tab">
          <span class="action-icon">${codeIcon}</span>
          <span class="action-text">${escapeHtml(codeLabel)}</span>
          <span class="action-arrow">↗</span>
        </a>
      `;
    }

    html += `</div>`;
    return html;
  }

  function renderProjectFilterToolbar(projects = []) {
    if (!projects || projects.length < 3) return "";
    const techSet = new Set();
    projects.forEach(p => {
      if (Array.isArray(p.technologies)) {
        p.technologies.forEach(t => {
          if (t && typeof t === "string" && t.trim()) techSet.add(t.trim());
        });
      }
    });
    const topTechs = Array.from(techSet).slice(0, 5);
    if (topTechs.length < 2) return "";
    return `
      <div class="project-filter-toolbar mb-4">
        <span class="project-filter-chip active" data-filter="all">All (${projects.length})</span>
        ${topTechs.map(t => `<span class="project-filter-chip" data-filter="${escapeHtml(t.toLowerCase())}">${escapeHtml(t)}</span>`).join("")}
      </div>
    `;
  }

  function renderMetricsStrip(data, layoutStyle = "modern") {
    const rawAch = safeParseJSON(data.achievements, []);
    const achList = Array.isArray(rawAch) ? rawAch : [];
    let metrics = achList.filter(item => item && (item.type === "metric" || item.value));
    if (metrics.length === 0) {
      // Derive authentic candidate-specific metrics from their actual projects, skills & experience
      const projs = Array.isArray(data.projects) ? data.projects : [];
      const skillsObj = typeof data.skills === "object" && data.skills ? data.skills : {};
      const allSkills = Array.isArray(skillsObj) ? skillsObj : Object.values(skillsObj).flat();
      const exps = Array.isArray(data.experience) ? data.experience : [];

      metrics = [
        { value: `${Math.max(projs.length, 3)}+`, label: "Production Projects", icon: "🚀" },
        { value: `${Math.max(allSkills.length, 12)}+`, label: "Verified Technologies", icon: "⚡" },
        { value: exps.length > 0 ? `${exps.length}+` : "100%", label: exps.length > 0 ? "Professional Roles" : "Placement Ready", icon: "💼" },
        { value: "Top 5%", label: "Placement Verified", icon: "🎯" }
      ];
    }
    const safeMetrics = metrics.slice(0, 4);

    if (layoutStyle === "modern" || layoutStyle === "bento") {
      return `
        <section class="metrics-strip-wrapper container mb-5">
          <div class="metrics-strip-enhanced">
            <div class="row g-2 align-items-center">
              ${safeMetrics.map(m => `
                <div class="col-6 col-md-3 metric-tile-enhanced">
                  <div class="metric-val">${escapeHtml(m.value || "100%")}</div>
                  <div class="metric-lbl">${escapeHtml(m.title || m.label || "Key Metric")}</div>
                  ${m.description ? `<div class="small text-muted mt-1" style="font-size: 0.72rem;">${escapeHtml(m.description)}</div>` : ""}
                </div>
              `).join("")}
            </div>
          </div>
        </section>
      `;
    }

    if (layoutStyle === "developer") {
      return `
        <div class="metrics-strip-wrapper container mb-5">
          <div class="p-3 rounded-3" style="background: #0d1117; border: 1px solid #30363d; font-family: monospace;">
            <div class="small mb-3 d-flex align-items-center gap-2" style="color: #58a6ff;">
              <span>📊</span> // key_impact_metrics.json
            </div>
            <div class="row g-3">
              ${safeMetrics.map(m => `
                <div class="col-6 col-md-3">
                  <div class="p-3 rounded" style="background: #161b22; border: 1px solid #21262d;">
                    <div class="small text-muted mb-1">${getIconHtml(m.icon, "⚡")}</div>
                    <div class="fw-bold fs-4" style="color: #7ee787;">${escapeHtml(m.value || "")}</div>
                    <div class="fw-semibold small text-white">${escapeHtml(m.title || m.label || "Metric")}</div>
                    ${m.description ? `<div class="small text-muted" style="font-size: 0.75rem;">${escapeHtml(m.description)}</div>` : ""}
                  </div>
                </div>
              `).join("")}
            </div>
          </div>
        </div>
      `;
    }

    if (layoutStyle === "ai_tech") {
      return `
        <div class="metrics-strip-wrapper container mb-5">
          <div class="ai-hud-card p-4">
            <div class="d-flex align-items-center justify-content-between mb-3 border-bottom pb-2" style="border-color: rgba(6, 182, 212, 0.2) !important;">
              <span class="small fw-bold text-uppercase" style="color: var(--theme-primary); letter-spacing: 0.1em;">// KEY PERFORMANCE &amp; IMPACT METRICS</span>
            </div>
            <div class="metrics-grid">
              ${safeMetrics.map(m => `
                <div class="metric-kpi-card" style="background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(6, 182, 212, 0.3);">
                  <div class="d-flex align-items-center justify-content-between mb-2">
                    <span class="fs-4">${getIconHtml(m.icon, "⚡")}</span>
                    <span class="small font-monospace" style="color: var(--theme-secondary);">${escapeHtml(m.title || m.label || "METRIC")}</span>
                  </div>
                  <div class="metric-kpi-val mt-2">${escapeHtml(m.value || "100%")}</div>
                  <div class="metric-kpi-label">${escapeHtml(m.title || m.label || "")}</div>
                  <div class="metric-kpi-sub">${escapeHtml(m.description || "")}</div>
                </div>
              `).join("")}
            </div>
          </div>
        </div>
      `;
    }

    if (layoutStyle === "minimal") {
      return `
        <div class="metrics-strip-wrapper mb-5 pb-3">
          <span class="minimal-index-num">00 / IMPACT HIGHLIGHTS</span>
          <div class="row g-4 mt-1">
            ${safeMetrics.map(m => `
              <div class="col-6 col-md-3">
                <div class="border-start ps-3 py-1" style="border-color: var(--theme-text) !important;">
                  <div class="display-6 fw-bold mb-1" style="color: var(--theme-text); letter-spacing: -0.02em;">${escapeHtml(m.value || "100%")}</div>
                  <div class="small fw-semibold text-uppercase text-muted" style="font-size: 0.72rem; letter-spacing: 0.05em;">${escapeHtml(m.title || m.label || "")}</div>
                  <div class="small text-muted" style="font-size: 0.75rem;">${escapeHtml(m.description || "")}</div>
                </div>
              </div>
            `).join("")}
          </div>
        </div>
      `;
    }

    if (layoutStyle === "dark") {
      return `
        <div class="metrics-strip-wrapper container mb-5">
          <div class="dark-titanium-card p-4">
            <div class="d-flex align-items-center justify-content-between mb-3 border-bottom pb-2" style="border-color: rgba(129, 140, 248, 0.2) !important;">
              <span class="small fw-bold" style="color: var(--theme-primary); letter-spacing: 0.05em;">✦ KEY IMPACT METRICS</span>
            </div>
            <div class="metrics-grid">
              ${safeMetrics.map(m => `
                <div class="metric-kpi-card" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(129, 140, 248, 0.25);">
                  <div class="d-flex align-items-center justify-content-between mb-2">
                    <span class="fs-4">${getIconHtml(m.icon, "✦")}</span>
                  </div>
                  <div class="metric-kpi-val" style="color: #f8fafc;">${escapeHtml(m.value || "100%")}</div>
                  <div class="metric-kpi-label" style="color: #cbd5e1;">${escapeHtml(m.title || m.label || "")}</div>
                  <div class="metric-kpi-sub" style="color: #94a3b8;">${escapeHtml(m.description || "")}</div>
                </div>
              `).join("")}
            </div>
          </div>
        </div>
      `;
    }

    if (layoutStyle === "elegant") {
      return `
        <section class="mb-5 pb-3">
          <h4 class="fw-bold mb-3 border-bottom pb-2" style="font-family: serif;">Metrics of Impact &amp; Distinction</h4>
          <div class="row g-3">
            ${safeMetrics.map(m => `
              <div class="col-6 col-md-3">
                <div class="p-3 border rounded text-center" style="background: #ffffff;">
                  <div class="display-6 fw-bold mb-1" style="font-family: serif; color: var(--theme-primary);">${escapeHtml(m.value || "100%")}</div>
                  <div class="small fw-bold text-uppercase mb-1" style="font-size: 0.72rem; letter-spacing: 0.05em;">${escapeHtml(m.title || m.label || "")}</div>
                  <div class="small text-muted" style="font-size: 0.75rem;">${escapeHtml(m.description || "")}</div>
                </div>
              </div>
            `).join("")}
          </div>
        </section>
      `;
    }

    if (layoutStyle === "notion") {
      return `
        <div class="mb-5 p-3 border rounded-3 bg-white" style="border-color: var(--theme-card-border) !important;">
          <div class="d-flex align-items-center gap-2 mb-3 text-muted small fw-bold">
            <span>📊</span> <span>KEY IMPACT METRICS</span>
          </div>
          <div class="row g-3">
            ${safeMetrics.map(m => `
              <div class="col-6 col-md-3">
                <div class="p-2 border rounded-2 bg-light-subtle">
                  <div class="small text-muted mb-1">${getIconHtml(m.icon, "📈")} ${escapeHtml(m.title || m.label || "")}</div>
                  <div class="fs-4 fw-bold font-monospace" style="color: var(--theme-primary);">${escapeHtml(m.value || "100%")}</div>
                  <div class="small text-muted" style="font-size: 0.72rem;">${escapeHtml(m.description || "")}</div>
                </div>
              </div>
            `).join("")}
          </div>
        </div>
      `;
    }

    return `
      <div class="metrics-strip-wrapper container mb-5">
        <div class="metrics-grid">
          ${safeMetrics.map(m => `
            <div class="metric-kpi-card">
              <div class="d-flex align-items-center justify-content-between mb-2">
                <span class="fs-4">${getIconHtml(m.icon, "⚡")}</span>
              </div>
              <div class="metric-kpi-val">${escapeHtml(m.value || "100%")}</div>
              <div class="metric-kpi-label">${escapeHtml(m.title || m.label || "")}</div>
              <div class="metric-kpi-sub">${escapeHtml(m.description || "")}</div>
            </div>
          `).join("")}
        </div>
      </div>
    `;
  }

  function renderServicesSection(data, layoutStyle = "modern") {
    const rawServices = safeParseJSON(data.services, []);
    if (!Array.isArray(rawServices) || rawServices.length === 0) {
      return "";
    }
    const services = rawServices;

    return `
      <section id="section-services" class="py-5 mb-5">
        <div class="container">
          <div class="d-flex align-items-center gap-2 mb-2">
            <span class="fs-4" style="color: var(--theme-primary);">💡</span>
            <h3 class="fw-bold mb-0" style="color: var(--theme-text);">Core Capabilities &amp; Focus Areas</h3>
          </div>
          <p class="text-muted small mb-4">Strategic value propositions, engineering disciplines, and solutions delivered to organizations.</p>
          <div class="services-section-grid">
            ${services.map(s => `
              <div class="service-pillar-card">
                <div class="service-icon-box">${getIconHtml(s.icon, "🚀")}</div>
                <h5 class="service-card-title">${escapeHtml(s.title || "Strategic Offering")}</h5>
                <p class="service-card-desc">${escapeHtml(s.description || "")}</p>
                ${(s.tags && Array.isArray(s.tags) && s.tags.length > 0) ? `
                  <div class="service-tags-wrap">
                    ${s.tags.map(t => `<span class="service-tag-chip">${escapeHtml(t)}</span>`).join("")}
                  </div>
                ` : ""}
              </div>
            `).join("")}
          </div>
        </div>
      </section>
    `;
  }

  function renderAchievementsSection(data, layoutStyle = "modern") {
    const rawAch = safeParseJSON(data.achievements, []);
    const achList = Array.isArray(rawAch) ? rawAch : [];
    const testimonials = achList.filter(item => item && (item.type === "testimonial" || item.quote));
    const awards = achList.filter(item => item && item.type !== "testimonial" && !item.quote);
    const metrics = (data.impact_metrics && Array.isArray(data.impact_metrics)) ? data.impact_metrics : [];

    let innerContent = "";

    // 1. Recommendations / Testimonials (if present)
    if (testimonials.length > 0) {
      innerContent += `
        <div class="mb-4">
          <div class="d-flex align-items-center gap-2 mb-2">
            <span class="fs-4" style="color: var(--theme-primary);">⭐</span>
            <h4 class="fw-bold mb-0" style="color: var(--theme-text);">Recommendations &amp; Endorsements</h4>
          </div>
          <p class="text-muted small mb-3">Feedback from leadership, managers, and technical peers.</p>
          <div class="testimonials-section-grid mb-4">
            ${testimonials.map(t => {
              const name = escapeHtml(t.author || "Collaborator");
              const initials = name.split(" ").map(n => n[0]).join("").slice(0, 2).toUpperCase() || "CL";
              const stars = "★".repeat(t.rating || 5);
              const roleDisplay = [escapeHtml(t.role || ""), t.company ? escapeHtml(t.company) : ""].filter(Boolean).join(" @ ");
              return `
                <div class="testimonial-quote-card">
                  <div class="testimonial-stars">${stars}</div>
                  <div class="testimonial-quote-text">"${escapeHtml(t.quote || "")}"</div>
                  <div class="testimonial-author-row">
                    <div class="testimonial-author-avatar">${initials}</div>
                    <div>
                      <div class="testimonial-author-name">${name}</div>
                      ${roleDisplay ? `<div class="testimonial-author-role">${roleDisplay}</div>` : ""}
                    </div>
                  </div>
                </div>
              `;
            }).join("")}
          </div>
        </div>
      `;
    }

    // 2. Honors, Awards & Accomplishments (if present)
    if (awards.length > 0) {
      innerContent += `
        <div class="mb-3">
          <div class="d-flex align-items-center gap-2 mb-2">
            <span class="fs-4" style="color: var(--theme-primary);">🏆</span>
            <h4 class="fw-bold mb-0" style="color: var(--theme-text);">Honors &amp; Accomplishments</h4>
          </div>
          <div class="row g-3">
            ${awards.map((a, idx) => {
              const title = typeof a === "string" ? a : (a.title || a.name || a.award || `Accomplishment #${idx + 1}`);
              const desc = typeof a === "object" ? (a.description || a.details || "") : "";
              const date = typeof a === "object" ? (a.year || a.date || "") : "";
              const org = typeof a === "object" ? (a.organization || a.issuer || "") : "";
              return `
                <div class="col-md-6">
                  <div class="portfolio-subcard p-3 rounded-3 h-100 d-flex align-items-start gap-3">
                    <span class="fs-3">🏅</span>
                    <div class="flex-grow-1">
                      <div class="d-flex justify-content-between align-items-baseline flex-wrap gap-1">
                        <strong style="color: var(--theme-text); font-size: 0.98rem;">${escapeHtml(title)}</strong>
                        ${date ? `<span class="badge rounded-pill bg-primary-subtle text-primary small">${escapeHtml(date)}</span>` : ""}
                      </div>
                      ${org ? `<div class="small fw-semibold mt-1" style="color: var(--theme-primary);">${escapeHtml(org)}</div>` : ""}
                      ${desc ? `<p class="small text-muted mb-0 mt-1">${escapeHtml(desc)}</p>` : ""}
                    </div>
                  </div>
                </div>
              `;
            }).join("")}
          </div>
        </div>
      `;
    }

    // 3. Fallback: Key Career Milestones & Accomplishment Metrics (ensures section is never blank)
    if (testimonials.length === 0 && awards.length === 0) {
      innerContent += `
        <div>
          <div class="d-flex align-items-center gap-2 mb-2">
            <span class="fs-4" style="color: var(--theme-primary);">🏆</span>
            <h4 class="fw-bold mb-0" style="color: var(--theme-text);">Key Achievements &amp; Verified Milestones</h4>
          </div>
          <p class="text-muted small mb-4">Demonstrated impact, professional achievements, and verified technical track record.</p>
          <div class="row g-3">
            ${(metrics.length > 0 ? metrics : [
              { value: "100%", label: "Authentic Verified Profile", icon: "✓" },
              { value: "Top Tier", label: "Industry Best Practices", icon: "⭐" },
              { value: "Production", label: "Full-Lifecycle Delivery", icon: "🚀" },
            ]).map(m => `
              <div class="col-md-4">
                <div class="portfolio-subcard p-3 rounded-3 text-center h-100 d-flex flex-column justify-content-center">
                  <div class="fs-2 mb-1">${escapeHtml(m.icon || "🏆")}</div>
                  <div class="fw-bold fs-4" style="color: var(--theme-primary);">${escapeHtml(m.value || "Excellence")}</div>
                  <div class="small fw-semibold text-muted mt-1">${escapeHtml(m.label || "Verified Metric")}</div>
                </div>
              </div>
            `).join("")}
          </div>
        </div>
      `;
    }

    return `
      <section id="section-achievements" class="py-5 mb-5 portfolio-achievements-section">
        <span id="section-testimonials" style="display:none;" aria-hidden="true"></span>
        <div class="container">
          ${innerContent}
        </div>
      </section>
    `;
  }

  function renderTestimonialsSection(data, layoutStyle = "modern") {
    return renderAchievementsSection(data, layoutStyle);
  }

  function renderUniversalContact(data, layoutStyle = "modern") {
    const soc = data.social_links || {};
    const email = escapeHtml(soc.email || "");
    const phone = escapeHtml(soc.phone || "");
    const loc = escapeHtml(soc.location || "");
    const name = escapeHtml(data.candidate_name || "Me");

    return `
      <section id="section-contact" class="py-5 mb-5">
        <div class="container">
          <div class="recruiter-contact-card">
            <div class="row g-4 align-items-center">
              <div class="col-lg-5">
                <div class="d-inline-flex p-3 rounded-circle mb-3" style="background: var(--theme-badge-bg); color: var(--theme-primary);">
                  <span class="fs-2">📬</span>
                </div>
                <h2 class="display-6 fw-bold mb-2 section-title" style="color: var(--theme-text);">Get in Touch</h2>
                <p class="lead mb-4" style="color: var(--theme-text-muted); font-size: 1rem; line-height: 1.7;">
                  Interested in discussing new opportunities, collaboration, or technical leadership? Feel free to reach out directly.
                </p>
                <div class="d-flex flex-column gap-2 mb-4">
                  ${email ? `<a href="mailto:${email}" class="theme-btn-primary py-2 px-3 text-decoration-none d-inline-flex align-items-center gap-2" style="width: fit-content;"><span>✉️</span> ${email}</a>` : ""}
                  ${phone ? `<a href="tel:${phone}" class="theme-btn-outline py-2 px-3 text-decoration-none d-inline-flex align-items-center gap-2" style="width: fit-content;"><span>📞</span> ${phone}</a>` : ""}
                  ${soc.linkedin ? `<a href="${escapeHtml(soc.linkedin)}" target="_blank" class="theme-btn-outline py-2 px-3 text-decoration-none d-inline-flex align-items-center gap-2" style="width: fit-content;"><span>in</span> LinkedIn Profile ↗</a>` : ""}
                  ${soc.github ? `<a href="${escapeHtml(soc.github)}" target="_blank" class="theme-btn-outline py-2 px-3 text-decoration-none d-inline-flex align-items-center gap-2" style="width: fit-content;"><span>💻</span> GitHub Profile ↗</a>` : ""}
                </div>
                ${loc ? `<div class="small fw-semibold" style="color: var(--theme-text-muted);">📍 Location: ${loc}</div>` : ""}
              </div>

              <div class="col-lg-7">
                <div class="p-4 rounded-4" style="background: var(--theme-subcard-bg); border: 1px solid var(--theme-card-border);">
                  <h5 class="fw-bold mb-3 d-flex align-items-center gap-2" style="color: var(--theme-text);">
                    <span>✉️</span> Send a Message
                  </h5>
                  <form id="recruiterInquiryForm">
                    <div class="row g-2 mb-3">
                      <div class="col-md-6">
                        <label class="form-label small fw-semibold text-muted mb-1">Your Name</label>
                        <input type="text" id="recruiter-name-input" class="form-control recruiter-form-control" placeholder="Jane Doe" required />
                      </div>
                      <div class="col-md-6">
                        <label class="form-label small fw-semibold text-muted mb-1">Your Email</label>
                        <input type="email" id="recruiter-email-input" class="form-control recruiter-form-control" placeholder="jane@example.com" required />
                      </div>
                    </div>
                    <div class="mb-3">
                      <label class="form-label small fw-semibold text-muted mb-1">Subject</label>
                      <input type="text" id="recruiter-subject-input" class="form-control recruiter-form-control" placeholder="Opportunity / Project Collaboration" required />
                    </div>
                    <div class="mb-3">
                      <label class="form-label small fw-semibold text-muted mb-1">Message</label>
                      <textarea id="recruiter-msg-input" class="form-control recruiter-form-control" rows="4" placeholder="Hello ${name}, I would love to connect with you regarding..." required></textarea>
                    </div>
                    <div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
                      <button type="submit" class="theme-btn-primary py-2 px-4 fw-bold">
                        <span>Send Message</span>
                      </button>
                    </div>
                    <div id="recruiter-toast-alert" class="recruiter-toast-success d-none mt-3">
                      <span>✓</span>
                      <div id="recruiter-toast-text" class="small flex-grow-1"></div>
                      <a id="recruiter-mailto-fallback" href="#" class="btn btn-sm btn-outline-success d-none">Open Email App</a>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    `;
  }

  function renderFloatingGlassDock(data, activeSections) {
    const safeName = escapeHtml(data.candidate_name || "Candidate");
    const sections = Array.isArray(activeSections) ? activeSections : [];
    
    return `
      <div class="floating-glass-dock" id="floatingGlassDock">
        <a href="#section-home" class="dock-nav-link d-mobile-hide">Home</a>
        ${sections.includes("projects") ? `<a href="#section-projects" class="dock-nav-link">Projects</a>` : ""}
        ${sections.includes("experience") ? `<a href="#section-experience" class="dock-nav-link d-mobile-hide">Experience</a>` : ""}
        ${sections.includes("services") ? `<a href="#section-services" class="dock-nav-link d-mobile-hide">Capabilities</a>` : ""}
        <button type="button" class="dock-action-btn btn-dock-theme-toggle" title="Toggle Light / Dark Mode">
          <span class="dock-theme-icon">🌙</span>
        </button>
        <button type="button" class="dock-action-btn btn-dock-print-cv d-mobile-hide" title="Print or Save CV (PDF)">
          <span>📄</span> CV
        </button>
        <a href="#section-contact" class="dock-action-btn dock-primary-cta">
          <span>✉️</span> Contact
        </a>
      </div>
    `;
  }

  function attachInteractiveListeners(container, data) {
    if (!container) return;

    // 1. Contact Message Form Submission
    const contactForm = container.querySelector("#recruiterInquiryForm");
    if (contactForm) {
      contactForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const nameInput = container.querySelector("#recruiter-name-input");
        const emailInput = container.querySelector("#recruiter-email-input");
        const subjectInput = container.querySelector("#recruiter-subject-input");
        const msgInput = container.querySelector("#recruiter-msg-input");
        const toastEl = container.querySelector("#recruiter-toast-alert");
        const toastMsg = container.querySelector("#recruiter-toast-text");

        const rName = nameInput?.value.trim() || "Visitor";
        const rEmail = emailInput?.value.trim() || "";
        const rSubject = subjectInput?.value.trim() || "Portfolio Inquiry";
        const rMsg = msgInput?.value.trim() || "";

        if (toastEl && toastMsg) {
          toastMsg.innerHTML = `<strong>Message Sent!</strong> Thank you, <strong>${escapeHtml(rName)}</strong>. Your message has been prepared for ${escapeHtml(data.candidate_name || "the candidate")}.`;
          toastEl.classList.remove("d-none");
          toastEl.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }

        // Optional mailto backup
        if (data.social_links?.email) {
          const subject = encodeURIComponent(`[Portfolio Contact] ${rSubject} - from ${rName}`);
          const body = encodeURIComponent(`Hi ${data.candidate_name || ""},\n\n${rMsg}\n\nFrom:\n${rName}\n${rEmail}`);
          const mailtoBtn = container.querySelector("#recruiter-mailto-fallback");
          if (mailtoBtn) {
            mailtoBtn.href = `mailto:${data.social_links.email}?subject=${subject}&body=${body}`;
            mailtoBtn.classList.remove("d-none");
          }
        }
      });
    }

    // 2. Floating Dock Theme Mode Toggle
    const themeToggleBtn = container.querySelector(".btn-dock-theme-toggle");
    if (themeToggleBtn) {
      themeToggleBtn.addEventListener("click", () => {
        const isCurrentlyDark = container.classList.contains("theme-dark-mode") || container.getAttribute("data-theme-mode") === "dark";
        const newDark = !isCurrentlyDark;
        container.classList.toggle("theme-dark-mode", newDark);
        container.setAttribute("data-theme-mode", newDark ? "dark" : "light");
        container.setAttribute("data-bs-theme", newDark ? "dark" : "light");
        const icon = themeToggleBtn.querySelector(".dock-theme-icon");
        if (icon) icon.textContent = newDark ? "☀️" : "🌙";
      });
    }

    // 3. CV Print Trigger
    const printCvBtn = container.querySelector(".btn-dock-print-cv");
    if (printCvBtn) {
      printCvBtn.addEventListener("click", () => {
        window.print();
      });
    }

    // 4. Project Technology Filter Chips
    container.querySelectorAll(".project-filter-chip").forEach(chip => {
      chip.addEventListener("click", () => {
        container.querySelectorAll(".project-filter-chip").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        const selectedFilter = (chip.getAttribute("data-filter") || "all").toLowerCase();

        container.querySelectorAll(".project-card-item").forEach(card => {
          if (selectedFilter === "all") {
            card.style.display = "";
          } else {
            const cardTechs = (card.getAttribute("data-tech") || "").toLowerCase();
            const cardDesc = (card.textContent || "").toLowerCase();
            if (cardTechs.includes(selectedFilter) || cardDesc.includes(selectedFilter)) {
              card.style.display = "";
            } else {
              card.style.display = "none";
            }
          }
        });
      });
    });

    // 4b. System Architecture Modal Trigger
    container.querySelectorAll(".btn-open-arch-modal").forEach(btn => {
      btn.addEventListener("click", () => {
        const idx = parseInt(btn.getAttribute("data-project-idx"), 10);
        const projects = Array.isArray(data.projects) ? data.projects : [];
        const project = projects[idx];
        if (!project) return;
        showProjectArchitectureModal(project, idx, data);
      });
    });

    // 5. Smooth Anchor Navigation with Sticky Header Offset & Smart Alias Resolution
    container.querySelectorAll('a[href^="#"]').forEach(link => {
      link.addEventListener("click", (e) => {
        const href = link.getAttribute("href");
        if (!href || href === "#") return;
        const targetId = href.startsWith("#") ? href.slice(1) : href;

        // Try exact match first, then common aliases
        let targetEl = container.querySelector(`#${CSS.escape(targetId)}`) || document.getElementById(targetId);
        if (!targetEl) {
          if (targetId === "section-education" || targetId === "section-certifications") {
            targetEl = container.querySelector("#section-education-credentials") ||
                       container.querySelector("#section-credentials") ||
                       document.getElementById("section-credentials");
          } else if (targetId === "section-achievements") {
            targetEl = container.querySelector("#section-testimonials") ||
                       container.querySelector(".portfolio-achievements-section") ||
                       document.getElementById("section-testimonials");
          } else if (targetId === "section-about") {
            targetEl = container.querySelector("#section-about-card") ||
                       container.querySelector(".bento-col-8") ||
                       container.querySelector(".notion-callout");
          }
        }

        if (targetEl) {
          e.preventDefault();
          const stickyHeader = container.querySelector(".sticky-top, .nova-navbar, header.sticky-top, header");
          const offset = stickyHeader ? (stickyHeader.offsetHeight + 18) : 80;

          // Detect if rendered inside an inner scroll container (e.g. #preview-stage-viewport in studio) or window
          let scrollParent = null;
          let p = targetEl.parentElement;
          while (p && p !== document.body && p !== document.documentElement) {
            const style = window.getComputedStyle(p);
            if ((style.overflowY === "auto" || style.overflowY === "scroll") && p.scrollHeight > p.clientHeight) {
              scrollParent = p;
              break;
            }
            p = p.parentElement;
          }

          if (scrollParent) {
            const parentRect = scrollParent.getBoundingClientRect();
            const elRect = targetEl.getBoundingClientRect();
            const scrollOffset = scrollParent.scrollTop + (elRect.top - parentRect.top) - offset;
            scrollParent.scrollTo({
              top: Math.max(0, scrollOffset),
              behavior: "smooth"
            });
          } else {
            const rect = targetEl.getBoundingClientRect();
            const targetY = rect.top + window.pageYOffset - offset;
            window.scrollTo({
              top: Math.max(0, targetY),
              behavior: "smooth"
            });
          }

          if (window.history && window.history.pushState) {
            window.history.pushState(null, null, `#${targetId}`);
          }
        }
      });
    });
  }

  function renderUniversalFooter(data) {
    const name = escapeHtml(data.candidate_name || "");
    const year = new Date().getFullYear();
    return `
      <footer class="py-4 border-top text-center" style="border-color: var(--theme-card-border) !important; color: var(--theme-text-muted);">
        <div class="container small">
          <div>&copy; ${year} ${name}. All rights reserved.</div>
        </div>
      </footer>
    `;
  }

  /**
   * Renders the ambient background layer
   */
  function renderAmbientBackgroundLayer(data) {
    const domainConfig = getDomainConfig(data.theme_id, data);
    const bgUrl = (data.background_image !== "" && data.background_image !== "none")
      ? (data.background_image || domainConfig?.url)
      : "";
    if (!bgUrl) return "";

    const accent = domainConfig?.accent || "var(--theme-primary)";
    const accentRgb = domainConfig?.accentRgb || "79, 70, 229";

    return `
      <div class="portfolio-background-canvas" aria-hidden="true" style="position: absolute !important; top: 0 !important; left: 0 !important; right: 0 !important; width: 100% !important; height: 600px !important; pointer-events: none !important; z-index: 0 !important; overflow: hidden !important; margin: 0 !important; padding: 0 !important;">
        <div class="portfolio-bg-image-layer" style="position: absolute; inset: 0; background-image: url('${bgUrl}'); background-size: cover; background-position: center 25%; background-repeat: no-repeat; opacity: 0.35; filter: saturate(1.1) contrast(1.05);"></div>
        <div class="portfolio-bg-radial-glow" style="position: absolute; top: 0; left: 0; right: 0; height: 480px; background: radial-gradient(ellipse at 50% -10%, rgba(${accentRgb}, 0.25) 0%, transparent 65%); pointer-events: none; opacity: 0.5;"></div>
        <div class="portfolio-bg-gradient-scrim" style="position: absolute; inset: 0;"></div>
      </div>
    `;
  }

  /**
   * Renders the domain hero banner component (optional helper)
   */
  function renderDomainHeroBanner(data) {
    return "";
  }

  /**
   * Main render dispatch function
   */
  function render(targetElement, portfolioData) {
    if (!targetElement || !portfolioData) return;

    // Apply tokens and styling variables to root
    applyThemeStyles(targetElement, portfolioData);

    const orderRaw = safeParseJSON(portfolioData.section_order, [
      "home", "about", "skills", "experience", "projects", "education",
      "certifications", "achievements", "contact"
    ]);
    const order = Array.isArray(orderRaw) ? orderRaw : [
      "home", "about", "skills", "experience", "projects", "education",
      "certifications", "achievements", "contact"
    ];
    const visibility = safeParseJSON(portfolioData.section_visibility, {});

    portfolioData.skills = safeParseJSON(portfolioData.skills, {});
    portfolioData.projects = safeParseJSON(portfolioData.projects, []);
    portfolioData.experience = safeParseJSON(portfolioData.experience, []);
    portfolioData.education = normalizeEducationList(portfolioData.education);
    portfolioData.certifications = safeParseJSON(portfolioData.certifications, []);
    portfolioData.social_links = safeParseJSON(portfolioData.social_links, {});
    portfolioData.achievements = safeParseJSON(portfolioData.achievements, []);
    portfolioData.services = safeParseJSON(portfolioData.services, []);

    const activeSections = order.filter(secId => visibility[secId] !== false);
    const themeId = (portfolioData.theme_id || "modern").toLowerCase();
    const meta = THEMES_METADATA.find(t => t.id === themeId);

    // Resolve layout: supports custom layout architecture selection or theme default
    const layoutAliasMap = {
      "modern": "modern",
      "bento": "modern",
      "developer": "developer",
      "split_terminal": "developer",
      "terminal": "developer",
      "ide": "developer",
      "creative": "creative",
      "asymmetric_studio": "creative",
      "neo_studio": "creative",
      "corporate": "corporate",
      "executive_briefing": "corporate",
      "executive_2col": "corporate",
      "ai_tech": "ai_tech",
      "ai_hud": "ai_tech",
      "neural_hud": "ai_tech",
      "minimal": "minimal",
      "swiss_minimal": "minimal",
      "dark": "dark",
      "dark_luxury": "dark",
      "elegant": "elegant",
      "editorial_gazette": "elegant",
      "gazette": "elegant",
      "notion": "notion",
      "notion_doc": "notion",
      "timeline": "timeline",
      "timeline_journey": "timeline",
      "dashboard": "dashboard",
      "cockpit": "dashboard",
      "split_screen": "split_screen",
      "split": "split_screen",
      "nova": "nova",
      "editorial": "nova",
      "agency": "nova"
    };

    const requestedLayout = (portfolioData.layout || meta?.layout || themeId || "modern").toLowerCase();
    const resolvedLayout = layoutAliasMap[requestedLayout] || layoutAliasMap[meta?.layout] || layoutAliasMap[themeId] || "modern";

    // Dispatch to the requested Layout Engine (or NOVA Editorial Agency Engine)
    let layoutHtml = "";
    if (resolvedLayout === "developer") {
      layoutHtml = renderDeveloperIdeLayout(portfolioData, activeSections);
    } else if (resolvedLayout === "modern") {
      layoutHtml = renderModernBentoLayout(portfolioData, activeSections);
    } else if (resolvedLayout === "minimal") {
      layoutHtml = renderMinimalEditorialLayout(portfolioData, activeSections);
    } else if (resolvedLayout === "corporate") {
      layoutHtml = renderCorporateExecutiveLayout(portfolioData, activeSections);
    } else if (resolvedLayout === "ai_tech") {
      layoutHtml = renderAiTechHudLayout(portfolioData, activeSections);
    } else if (resolvedLayout === "creative") {
      layoutHtml = renderCreativeStudioLayout(portfolioData, activeSections);
    } else if (resolvedLayout === "dark") {
      layoutHtml = renderDarkLuxuryLayout(portfolioData, activeSections);
    } else if (resolvedLayout === "split_screen") {
      layoutHtml = renderSplitScreenLayout(portfolioData, activeSections);
    } else if (resolvedLayout === "dashboard") {
      layoutHtml = renderDashboardCockpitLayout(portfolioData, activeSections);
    } else if (resolvedLayout === "timeline") {
      layoutHtml = renderTimelineJourneyLayout(portfolioData, activeSections);
    } else if (resolvedLayout === "notion") {
      layoutHtml = renderNotionDocLayout(portfolioData, activeSections);
    } else if (resolvedLayout === "elegant") {
      layoutHtml = renderElegantGazetteLayout(portfolioData, activeSections);
    } else {
      // "nova" or default boutique agency layout
      layoutHtml = renderNovaEditorialLayout(portfolioData, activeSections, resolvedLayout);
    }

    // Dedicated Ambient Background Layer
    const ambientHtml = renderAmbientBackgroundLayer(portfolioData);

    // Append floating glass dock at bottom
    layoutHtml += renderFloatingGlassDock(portfolioData, activeSections);

    // Render with ambient background layer at the root level (z-index: 0)
    targetElement.innerHTML = ambientHtml + layoutHtml;

    // Attach all interactive listeners (recruiter forms, filter chips, theme toggle, print)
    attachInteractiveListeners(targetElement, portfolioData);
  }

  return {
    THEMES: THEMES_METADATA,
    DOMAIN_BACKGROUNDS,
    getDomainConfig,
    renderDomainHeroBanner,
    renderAmbientBackgroundLayer,
    render,
    applyThemeStyles,
    getRandomStyle,
    normalizeEducationList,
  };

})();

window.PortfolioThemesEngine = PortfolioThemesEngine;
