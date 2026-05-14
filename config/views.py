from django.http import Http404
from django.shortcuts import render


INFO_ARTICLES = [
    {
        "slug": "furniture-materials",
        "title": "Furniture materials",
        "image_url": "/media/info/furniture-materials-header.png",
        "intro": (
            "A guide to common furniture materials, including textile, wood, metal, "
            "plastic, leather, artificial leather, glass, steel, concrete, marble, "
            "bronze, and stone."
        ),
        "paragraphs": [
            "Furniture Materials:",
            (
                "Textile: Textile materials include fabrics such as cotton, linen, wool, "
                "and polyester used for upholstery and decoration. They provide comfort, "
                "texture, color, and pattern in furniture design."
            ),
            (
                "Wood: Wood is one of the most traditional and versatile furniture materials. "
                "It is valued for its strength, durability, natural grain patterns, and ability "
                "to fit both classic and modern styles."
            ),
            (
                "Metal: Metal furniture materials include aluminum, iron, brass, and other "
                "alloys. Metal is known for its strength, durability, and sleek appearance, "
                "often used in industrial and modern furniture."
            ),
            (
                "Plastic: Plastic is a lightweight and versatile material commonly used in "
                "contemporary furniture. It can be molded into many shapes and colors while "
                "remaining durable and affordable."
            ),
            (
                "Leather: Leather is a durable natural material made from animal hide. It is "
                "commonly used in furniture upholstery for its luxurious appearance, comfort, "
                "and long-lasting quality."
            ),
            (
                "Artificial Leather: Artificial leather, also known as synthetic or faux leather, "
                "is a man-made alternative to real leather. It offers a similar appearance and "
                "texture while often being more affordable and easier to maintain."
            ),
            (
                "Glass: Glass is used in furniture for tabletops, shelves, and decorative "
                "elements. It creates a modern, elegant appearance and can make spaces feel "
                "lighter and more open."
            ),
            (
                "Steel: Steel is a strong and durable metal frequently used in modern and "
                "industrial furniture design. It provides structural support and a clean, "
                "contemporary look."
            ),
            (
                "Concrete: Concrete is a heavy and durable material used in modern and "
                "minimalist furniture. It is valued for its raw texture, industrial appearance, "
                "and strength."
            ),
            (
                "Marble: Marble is a natural stone known for its smooth surface and distinctive "
                "veining. It is commonly used in luxury furniture for tabletops and decorative "
                "elements."
            ),
            (
                "Bronze: Bronze is a metal alloy often used for decorative furniture details "
                "and artistic elements. It is appreciated for its durability and warm metallic "
                "appearance."
            ),
            (
                "Stone: Stone is a natural material used in furniture for its durability, "
                "texture, and timeless appearance. Different stone types provide unique colors, "
                "patterns, and finishes."
            ),
        ],
    },
    {
        "slug": "furniture-styles",
        "title": "Furniture styles",
        "image_url": "/media/built-in_artworks/Furniture.jpeg",
        "intro": (
            "A guide to furniture styles, including contemporary, Art Deco, "
            "minimalism, Renaissance, modernism, Baroque, maximalism, classicism, "
            "and postmodernism."
        ),
        "paragraphs": [
            "Furniture Styles:",
            (
                "Contemporary: Contemporary furniture reflects current design trends "
                "and often combines simplicity, comfort, and functionality. It commonly "
                "features clean lines, neutral colors, and a mix of natural and modern "
                "materials."
            ),
            (
                "Art Deco: Art Deco furniture is known for its luxury, bold geometric "
                "patterns, rich materials, and decorative details. Popular during the "
                "1920s and 1930s, it often uses glossy finishes, metallic accents, and "
                "symmetrical designs."
            ),
            (
                "Minimalism: Minimalist furniture emphasizes simplicity, clean forms, "
                "and functionality. It avoids unnecessary decoration and focuses on "
                "open space, neutral colors, and practical design."
            ),
            (
                "Renaissance: Renaissance furniture was inspired by classical Greek "
                "and Roman art and architecture. It often features carved wood, symmetry, "
                "elegant proportions, and detailed ornamentation reflecting wealth and "
                "craftsmanship."
            ),
            (
                "Modernism: Modernist furniture focuses on function, innovation, and "
                "simplicity. Emerging in the early 20th century, it introduced clean "
                "lines, industrial materials, and designs that prioritize practicality "
                "over decoration."
            ),
            (
                "Baroque: Baroque furniture is dramatic, ornate, and highly decorative. "
                "It often includes curved forms, rich fabrics, gilded details, and "
                "elaborate carvings designed to convey luxury and grandeur."
            ),
            (
                "Maximalism: Maximalist furniture embraces bold colors, layered textures, "
                "decorative patterns, and visual richness. The style values individuality "
                "and abundance rather than simplicity or restraint."
            ),
            (
                "Classicism: Classical furniture is inspired by the balanced proportions "
                "and elegance of ancient Greek and Roman design. It often includes "
                "symmetrical forms, refined decoration, and timeless craftsmanship."
            ),
            (
                "Postmodernism: Postmodern furniture challenges traditional design rules "
                "through playful shapes, bold colors, and unconventional combinations of "
                "materials. It often mixes historical references with modern experimentation "
                "and humor."
            ),
        ],
    },
    {
        "slug": "sculpture-mediums",
        "title": "Sculpture mediums",
        "image_url": "/media/info/sculpture-mediums-header.png",
        "intro": (
            "A guide to common sculpture mediums, including bronze, marble, "
            "wood, and clay."
        ),
        "paragraphs": [
            "Sculpture Mediums:",
            (
                "Bronze: Bronze is a durable metal alloy commonly used in sculpture "
                "casting. It allows for fine detail, strength, and long-lasting outdoor "
                "sculptures, often developing a natural patina over time."
            ),
            (
                "Marble: Marble is a smooth, fine-grained stone widely used in classical "
                "sculpture. It is valued for its elegance, durability, and ability to "
                "capture detailed carving and polished surfaces."
            ),
            (
                "Wood: Wood is a versatile sculptural material that can be carved, "
                "assembled, or shaped into many forms. Different wood types provide "
                "unique textures, colors, and grain patterns."
            ),
            (
                "Clay: Clay is a soft and flexible material commonly used for modeling "
                "sculptures. It allows artists to easily shape and refine forms before "
                "the work is dried or fired into ceramic."
            ),
        ],
    },
    {
        "slug": "sculpture-styles",
        "title": "Sculpture styles",
        "image_url": "/media/info/sculpture-styles-header.png",
        "intro": (
            "A guide to sculpture styles, from abstract, relief, freestanding, "
            "carved, modeled, assembled, and cast sculpture to modern, classical, "
            "baroque, hyperrealist, futuristic, and gothic approaches."
        ),
        "paragraphs": [
            "Sculpture Styles:",
            (
                "Abstract: Abstract sculpture focuses on shapes, forms, textures, "
                "and movement rather than realistic representation. It often "
                "simplifies or distorts subjects to emphasize artistic expression "
                "and visual impact."
            ),
            (
                "Relief: Relief sculpture is attached to a flat surface, with "
                "figures or forms projecting outward from the background. It is "
                "commonly used on walls, monuments, and architectural decorations."
            ),
            (
                "Freestanding: Freestanding sculpture is fully three-dimensional "
                "and can be viewed from all angles. Unlike relief sculpture, it is "
                "not connected to a background surface."
            ),
            (
                "Carved: Carved sculpture is created by removing material from a "
                "solid block such as stone, wood, or marble. Artists shape the work "
                "through chiseling, cutting, or scraping techniques."
            ),
            (
                "Modeling: Modeling is a sculptural process where soft materials "
                "like clay or wax are shaped and built up by hand. It allows artists "
                "to easily alter and refine forms."
            ),
            (
                "Assembled: Assembled sculpture is made by combining separate "
                "materials or found objects into one artwork. Artists often use "
                "metal, wood, plastic, or industrial materials in the construction."
            ),
            (
                "Cast: Cast sculpture is produced by pouring liquid material such "
                "as bronze, plaster, or resin into a mold. Once hardened, the "
                "sculpture is removed and finished."
            ),
            (
                "Minimalism: Minimalist sculpture emphasizes simplicity, clean lines, "
                "and geometric forms. The style removes unnecessary detail to focus "
                "on shape, space, and material."
            ),
            (
                "Constructivism: Constructivist sculpture uses geometric structures "
                "and industrial materials to create modern, engineered forms. It "
                "emphasizes order, functionality, and technological progress."
            ),
            (
                "Surrealism: Surrealist sculpture explores dreams, fantasy, and the "
                "subconscious mind. It often combines unusual forms and symbolic "
                "imagery to create imaginative and unexpected works."
            ),
            (
                "Kinetic Art: Kinetic sculpture incorporates movement into the artwork. "
                "The motion may be powered by wind, motors, light, or viewer interaction, "
                "creating dynamic visual effects."
            ),
            (
                "Contemporary: Contemporary sculpture refers to sculpture created from "
                "the late 20th century to the present day. It includes a wide range of "
                "materials, concepts, and experimental techniques that often address "
                "modern social and cultural themes."
            ),
            (
                "Figurative Art: Figurative sculpture represents recognizable human or "
                "animal forms. It may be realistic or stylized but maintains a clear "
                "connection to real-life subjects."
            ),
            (
                "Modern Art: Modern sculpture developed during the late 19th and early "
                "20th centuries and focused on experimentation and innovation. Artists "
                "explored abstraction, new materials, and simplified forms."
            ),
            (
                "Modernism: Modernist sculpture rejected traditional artistic conventions "
                "and embraced new ideas, abstraction, and industrial materials. It "
                "emphasized originality and the exploration of form and structure."
            ),
            (
                "Cubism: Cubist sculpture breaks subjects into fragmented geometric forms "
                "and presents multiple viewpoints at once. The style creates structured "
                "and abstract compositions."
            ),
            (
                "Baroque: Baroque sculpture is dramatic, emotional, and highly detailed. "
                "It often features movement, flowing drapery, and theatrical poses to "
                "create energy and intensity."
            ),
            (
                "Renaissance: Renaissance sculpture emphasized realism, proportion, "
                "anatomy, and balance inspired by classical Greek and Roman art. Artists "
                "aimed to create lifelike human figures and harmonious compositions."
            ),
            (
                "Classicism: Classical sculpture is based on the ideals of ancient Greece "
                "and Rome, emphasizing symmetry, proportion, beauty, and idealized human "
                "forms."
            ),
            (
                "Hyperrealism: Hyperrealist sculpture is created with extreme precision "
                "to closely resemble real life. Artists reproduce realistic skin textures, "
                "facial expressions, clothing, and fine details."
            ),
            (
                "Concrete Art: Concrete sculpture is entirely non-representational and "
                "focuses on geometric forms, mathematical structure, and visual balance "
                "rather than symbolic meaning or realism."
            ),
            (
                "Futurism: Futurist sculpture celebrates speed, technology, machinery, "
                "and movement. Artists use dynamic lines and repeated forms to suggest "
                "motion and energy."
            ),
            (
                "Gothic Art: Gothic sculpture developed during the medieval period and "
                "is commonly associated with cathedrals and religious architecture. It "
                "features elongated figures, intricate detail, and spiritual themes."
            ),
        ],
    },
    {
        "slug": "photo-styles-and-techniques",
        "title": "Photo styles and techniques",
        "image_url": "/media/info/photo-styles-header.png",
        "intro": (
            "A guide to common photography styles and techniques, including "
            "landscape, portrait, fashion, black and white, astrophotography, "
            "aerial, editorial, food, architectural, nature, sports, abstract, "
            "digital, and film photography."
        ),
        "paragraphs": [
            "Photo Styles:",
            (
                "Landscape: Landscape photography captures natural scenery such "
                "as mountains, forests, oceans, and valleys. It often emphasizes "
                "atmosphere, lighting, and the beauty of the environment."
            ),
            (
                "Portrait: Portrait photography focuses on capturing the personality, "
                "emotion, and expression of a person or group of people. It can be "
                "posed or candid and often highlights facial features and mood."
            ),
            (
                "Fashion: Fashion photography is used to showcase clothing, accessories, "
                "and beauty products. It is commonly seen in magazines, advertisements, "
                "and brand campaigns, often using stylized poses and creative settings."
            ),
            (
                "Black and White: Black and white photography removes color to emphasize "
                "contrast, texture, shape, and emotion. The style is often used to create "
                "dramatic, timeless, or artistic images."
            ),
            (
                "Astrophotography: Astrophotography captures celestial objects and night "
                "skies, including stars, planets, galaxies, and the Milky Way. It often "
                "requires long exposure techniques and specialized equipment."
            ),
            (
                "Aerial: Aerial photography is taken from an elevated position, such as "
                "a drone, airplane, or helicopter. It provides unique perspectives of "
                "landscapes, cities, and environments from above."
            ),
            (
                "Editorial: Editorial photography tells a story or supports written content "
                "in magazines, newspapers, or online publications. The images are often "
                "realistic, narrative-driven, and connected to current events or themes."
            ),
            (
                "Food: Food photography focuses on presenting food and beverages in an "
                "appealing and visually attractive way. Lighting, composition, and styling "
                "are important elements in this style."
            ),
            (
                "Architectural: Architectural photography captures buildings, interiors, "
                "and structures with attention to design, symmetry, and form. It is commonly "
                "used in real estate, design portfolios, and documentation."
            ),
            (
                "Headshot: Headshot photography is a close-up portrait style primarily "
                "focused on the face. It is commonly used for professional profiles, acting "
                "portfolios, and business purposes."
            ),
            (
                "Nature: Nature photography documents wildlife, plants, landscapes, and "
                "natural environments. It often aims to highlight the beauty, diversity, "
                "and detail of the natural world."
            ),
            (
                "Sports: Sports photography captures athletes, competitions, and moments "
                "of action. It often uses fast shutter speeds to freeze movement and convey "
                "energy and intensity."
            ),
            (
                "Conceptual: Conceptual photography is designed to communicate an idea, "
                "message, or emotion rather than simply document reality. It often uses "
                "symbolism, creative staging, and visual storytelling."
            ),
            (
                "Abstract: Abstract photography focuses on shapes, colors, textures, patterns, "
                "and forms instead of recognizable subjects. It encourages interpretation and "
                "experimentation with composition."
            ),
            "Photo Techniques:",
            (
                "Digital: Digital photography uses electronic sensors to capture images that "
                "are stored digitally. It allows instant image review, editing, and easy "
                "sharing through digital devices."
            ),
            (
                "Film: Film photography captures images on light-sensitive photographic film. "
                "It is known for its organic grain, tonal depth, and traditional development "
                "process in a darkroom."
            ),
        ],
    },
    {
        "slug": "painting-mediums",
        "title": "Painting mediums",
        "image_url": "/media/info/painting-mediums-header.png",
        "intro": (
            "A guide to common painting mediums, including oil, watercolor, "
            "acrylic, gouache, encaustic, tempera, fresco, ink, charcoal, "
            "chalk, graphite, and spray painting."
        ),
        "paragraphs": [
            (
                "Oil Painting: Oil painting uses pigments mixed with oil, "
                "usually linseed oil, to create rich colors and smooth blending. "
                "It dries slowly, allowing artists to build layers and fine "
                "details over time."
            ),
            (
                "Watercolor Painting: Watercolor painting uses water-based "
                "pigments applied in transparent layers. It is known for its "
                "soft appearance, fluid textures, and delicate color transitions."
            ),
            (
                "Acrylic Painting: Acrylic painting uses fast-drying synthetic "
                "paint that can mimic both oil and watercolor effects. It is "
                "versatile, durable, and commonly used in both traditional and "
                "contemporary art."
            ),
            (
                "Gouache: Gouache is an opaque water-based paint with a matte "
                "finish. It produces bold, solid colors and is often used for "
                "illustrations, design work, and fine art."
            ),
            (
                "Encaustic: Encaustic painting involves mixing pigments with "
                "heated wax and applying them to a surface. The technique creates "
                "textured, luminous artworks with strong durability."
            ),
            (
                "Tempera: Tempera uses pigments mixed with a binder such as egg "
                "yolk. It dries quickly and produces precise details and smooth, "
                "flat areas of color."
            ),
            (
                "Fresco: Fresco is a mural painting technique where pigments are "
                "applied onto freshly laid wet plaster. As the plaster dries, the "
                "painting becomes part of the wall surface."
            ),
            (
                "Ink: Ink is a liquid medium used for drawing, writing, and "
                "painting. It can create sharp lines, strong contrast, and "
                "expressive brushwork."
            ),
            (
                "Charcoal: Charcoal is a dry drawing medium made from burned wood "
                "or organic material. It is valued for its deep black tones, soft "
                "shading, and expressive marks."
            ),
            (
                "Chalk: Chalk is a soft drawing medium often used for sketching "
                "and shading. It can produce smooth textures and subtle tonal "
                "effects, especially on colored paper."
            ),
            (
                "Graphite: Graphite is the material commonly found in pencils and "
                "is used for drawing and sketching. It allows for precise detail, "
                "shading, and a wide range of tones."
            ),
            (
                "Spray Painting: Spray painting uses aerosol paint applied through "
                "a spray can or spray gun. It is widely associated with street art "
                "and graffiti but is also used in fine art and large-scale murals."
            ),
        ],
    },
    {
        "slug": "painting-styles",
        "title": "Painting styles",
        "image_url": "/media/info/painting-styles-header.png",
        "intro": (
            "A guide to major painting styles, from Renaissance and Baroque "
            "to Impressionism, Abstract Art, Pop Art, and Contemporary Art."
        ),
        "paragraphs": [
            (
                "Renaissance (1350-1620): The Renaissance was a cultural movement "
                "that began in Italy and emphasized a revival of classical knowledge "
                "from ancient Greece and Rome. Renaissance art focused on realism, "
                "balance, perspective, anatomy, and human emotion. Artists aimed to "
                "create lifelike figures and harmonious compositions using mathematical "
                "proportion and linear perspective. Religious themes were still common, "
                "but artists increasingly celebrated humanism, science, and individual "
                "achievement."
            ),
            (
                "Baroque (1600 - 1750): Baroque art was dramatic, emotional, and "
                "highly detailed. Emerging after the Renaissance, it used strong "
                "contrasts between light and shadow, dynamic movement, and theatrical "
                "compositions to create intensity and grandeur. Baroque artists often "
                "painted religious, mythological, and historical scenes with realism "
                "and emotional depth. The style was closely associated with the Catholic "
                "Counter-Reformation and the power of European monarchies."
            ),
            (
                "Rococo (Early 18th century): Rococo developed in France as a lighter "
                "and more decorative reaction to the seriousness of Baroque art. It "
                "featured soft pastel colors, playful themes, elegant curves, and "
                "romantic or aristocratic subjects. Rococo paintings often depicted "
                "leisure, love, and fantasy in luxurious settings, reflecting the "
                "lifestyle of the French upper class before the French Revolution."
            ),
            (
                "Neoclassicism (1760s - 1840s): Neoclassicism was inspired by the art "
                "and ideals of ancient Greece and Rome. It emerged partly as a reaction "
                "against the excess and ornamentation of Rococo art. Neoclassical artists "
                "emphasized order, discipline, symmetry, and moral virtue. Paintings often "
                "portrayed heroic historical or mythological scenes with clean lines, "
                "balanced compositions, and restrained emotion."
            ),
            (
                "Romanticism (1750 - 1890): Romanticism focused on emotion, imagination, "
                "individuality, and the power of nature. Romantic artists rejected strict "
                "rationality and instead explored dramatic landscapes, exotic subjects, "
                "historical events, and intense human feelings. Their works often emphasized "
                "mystery, heroism, and the sublime beauty and danger of the natural world."
            ),
            (
                "Realism (1840s - 1880s): Realism aimed to depict everyday life truthfully "
                "without idealization or dramatic exaggeration. Realist artists painted "
                "ordinary people, workers, and social realities with accurate detail and "
                "natural colors. The movement challenged the romanticized subjects of "
                "earlier styles and reflected the social and political changes of the "
                "industrial era."
            ),
            (
                "Impressionism (1867 - 1886): Impressionism focused on capturing fleeting "
                "moments, light, atmosphere, and movement. Artists used loose brushstrokes, "
                "bright colors, and outdoor painting techniques to portray modern life and "
                "natural scenery. Instead of detailed realism, Impressionists emphasized the "
                "visual impression of a scene, especially how light changes over time."
            ),
            (
                "Post-Impressionism (1886 - 1905): Post-Impressionism built upon "
                "Impressionist techniques but explored stronger structure, symbolism, "
                "emotion, and color experimentation. Artists developed highly individual "
                "styles that moved beyond simply capturing light and atmosphere. The "
                "movement paved the way for modern art by emphasizing personal expression "
                "and abstraction."
            ),
            (
                "Expressionism (1905 - 1920): Expressionism prioritized emotional expression "
                "over realistic representation. Artists distorted shapes, exaggerated colors, "
                "and used energetic brushwork to communicate inner feelings, anxiety, or "
                "psychological tension. Expressionist works were often intense, dramatic, "
                "and deeply personal, reflecting the uncertainties of the modern world."
            ),
            (
                "Fauvism (1905 - 1908): Fauvism was characterized by bold, non-naturalistic "
                "colors and simplified forms. Fauvist artists used vivid color primarily "
                "for emotional and visual impact rather than realism. Their paintings were "
                "energetic, expressive, and experimental, helping push art toward abstraction "
                "and modernism."
            ),
            (
                "Cubism (1907 - 1914): Cubism revolutionized art by breaking subjects into "
                "geometric shapes and showing multiple viewpoints simultaneously. Instead of "
                "creating realistic depth, Cubist artists flattened space and fragmented "
                "objects into abstract forms. The movement challenged traditional perspective "
                "and became one of the foundations of modern art."
            ),
            (
                "Surrealism (1920s - now): Surrealism explored dreams, the subconscious mind, "
                "and irrational imagery. Influenced by psychoanalysis, Surrealist artists "
                "combined unexpected objects and fantastical scenes to challenge logic and "
                "reality. Their works often appear strange, symbolic, or dreamlike, encouraging "
                "viewers to interpret hidden meanings."
            ),
            (
                "Abstract Art (1910s - now): Abstract art moves away from direct representation "
                "of reality and instead focuses on color, shape, form, texture, and composition. "
                "Some abstract works are inspired by real subjects, while others are completely "
                "non-representational. The style emphasizes artistic freedom, experimentation, "
                "and emotional or conceptual expression."
            ),
            (
                "Futurism (1909 - 1944): Futurism celebrated speed, technology, industry, "
                "and modern urban life. Originating in Italy, Futurist artists portrayed "
                "movement, machinery, energy, and progress through dynamic compositions and "
                "repeated forms. The movement reflected fascination with modernity and the "
                "rapid changes of the industrial age."
            ),
            (
                "Pop Art (1950s - 1960s): Pop Art drew inspiration from popular culture, "
                "advertising, comics, and mass media. Artists used recognizable commercial "
                "imagery, bold colors, and repetition to blur the boundaries between high art "
                "and everyday consumer culture. Pop Art often explored themes of celebrity, "
                "consumerism, and media influence with humor and irony."
            ),
            (
                "Minimalism (1960s - now): Minimalism emphasized simplicity, order, and "
                "reduction of form. Minimalist artists removed unnecessary detail and focused "
                "on basic geometric shapes, clean lines, and limited color palettes. The "
                "movement aimed to create clarity and direct visual experience rather than "
                "emotional storytelling or symbolism."
            ),
            (
                "Photorealism (late 1960s - early 1970s): Photorealism sought to create "
                "paintings and drawings that looked almost identical to photographs. Artists "
                "used extreme precision, fine detail, and careful observation to reproduce "
                "reflections, textures, and lighting realistically. The movement explored the "
                "relationship between photography and traditional painting techniques."
            ),
            (
                "Contemporary Art (1970s - now): Contemporary art refers to art created from "
                "the late 20th century to the present day. It includes a wide variety of styles, "
                "techniques, and concepts, often addressing social, political, cultural, or "
                "technological issues. Contemporary artists experiment with traditional and "
                "digital media, installation, performance, and conceptual approaches, reflecting "
                "the diversity and complexity of modern society."
            ),
        ],
    },
]


def info_view(request):
    return render(request, "info.html", {"articles": INFO_ARTICLES})


def info_article_view(request, slug):
    article = next(
        (article_item for article_item in INFO_ARTICLES if article_item["slug"] == slug),
        None,
    )

    if article is None:
        raise Http404("Article not found")

    article = article.copy()
    article["formatted_paragraphs"] = [
        paragraph.split(":", 1)
        if ":" in paragraph
        else [None, paragraph]
        for paragraph in article["paragraphs"]
    ]

    return render(request, "info_article.html", {"article": article})
