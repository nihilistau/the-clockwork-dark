/* The Clockwork Dark — world bible data.
   Drawn from data/lore/*.md, data/economy.yaml, data/procgen_templates/comfyui.yaml.
   Painterly placeholders are tuned per subject; production art is ComfyUI at runtime. */

window.CW_DATA = {

  // ---------------------------------------------------------------
  // PLACES & BUILDINGS  (location_still 16:9, 1344×768)
  // ---------------------------------------------------------------
  places: [
    {
      id: "forest_clearing", name: "The Forest Clearing", kind: "Wilds",
      tint: "linear-gradient(165deg,#324233 0%,#46553d 40%,#6d6a48 72%,#9a9258 100%)",
      glow: "radial-gradient(120% 80% at 50% 12%, rgba(232,196,122,.30), transparent 58%)",
      caption: "Birch margin · dawn mist",
      img: "../../assets/art/scenes/forest-mushroom-ring.jpg",
      blurb: "Where travelers wake. Birch and fern, mushroom circles, game trails that double back when watched. Smoke from Edgewood drifts west even when the wind blows south.",
      times: ["dawn mist", "noon", "blue hour"],
      prompt: "misty birch forest clearing, distant village smoke, mushrooms, ferns",
      note: "No minimap. Things watch from stillness without moving."
    },
    {
      id: "edgewood_square", name: "Edgewood Square", kind: "Village",
      tint: "linear-gradient(165deg,#2c3a2a 0%,#4a4732 48%,#6e5a39 80%,#8a6b3f 100%)",
      glow: "radial-gradient(120% 80% at 62% 18%, rgba(232,196,122,.34), transparent 55%)",
      caption: "Communal oven · evening",
      img: "../../assets/art/scenes/town-scene.jpg",
      blurb: "Timber frames lean together around the communal stone oven. A shrine to unnamed saints never lacks a candle — though nobody can name the saints.",
      times: ["market day", "quiet evening"],
      prompt: "frontier village square, timber houses, communal stone oven, chickens",
      note: "NPC markers subtle — name on hover, never gamey icons."
    },
    {
      id: "edgewood_bakery", name: "The Hearth Bakery", kind: "Interior",
      tint: "linear-gradient(165deg,#3a2a1f 0%,#6b4524 45%,#a9692f 76%,#e0a851 100%)",
      glow: "radial-gradient(90% 90% at 30% 60%, rgba(232,196,122,.46), transparent 60%)",
      caption: "Brick oven · morning prep",
      img: "../../assets/art/scenes/bakery.jpg",
      blurb: "Maris Hearth runs it with flour on her sleeves and a hum in her throat. Villagers say she hums to keep the gears quiet. Loaves that taste of honest hunger, not prophecy.",
      times: ["morning prep", "night, empty"],
      prompt: "small bakery interior, brick oven, flour sacks, warm light",
      note: "Domestic UI (recipes, oven timer) must look as polished as adventure UI."
    },
    {
      id: "tinker_caravan", name: "The Tinker Caravan", kind: "Caravan",
      tint: "linear-gradient(165deg,#33281f 0%,#5a4128 46%,#8a5a2f 78%,#b8863f 100%)",
      glow: "radial-gradient(110% 80% at 50% 30%, rgba(201,122,60,.34), transparent 60%)",
      caption: "Nine-pin tent · arrival sunset",
      img: "../../assets/art/scenes/tinker-cart.jpg",
      blurb: "Ilya's wagon: tools, maps, hanging charms, chalk symbols, suspicious sympathy lamps. Maps of roads that shift when the wheat turns wrong.",
      times: ["arrival sunset", "rainy pack-up"],
      prompt: "colorful tinker tent, brass charms, maps, wagon wheels",
      note: "Trade UI is a barter list — not gold coins floating."
    },
    {
      id: "millhaven_gate", name: "Millhaven Gate", kind: "Frontier",
      tint: "linear-gradient(165deg,#2a3036 0%,#43505a 46%,#5e6a6e 76%,#8a9088 100%)",
      glow: "radial-gradient(120% 90% at 50% 20%, rgba(180,190,190,.22), transparent 60%)",
      caption: "Palisade · cold rain",
      img: "../../assets/art/scenes/closing-town-gates.jpg",
      blurb: "A wooden palisade gate, militia banners, mud road, refugees. Sergeant Sera holds the line — duty-heavy, not a villain.",
      times: ["rain", "clear cold morning"],
      prompt: "wooden palisade gate, militia banners, mud road, refugees",
      note: "Rain variant; wrong_rain (falls upward) only STIRRING+."
    },
    {
      id: "corruption_border", name: "The Corruption Border", kind: "Wrongness",
      tint: "linear-gradient(165deg,#222a1c 0%,#3c4a26 44%,#5e6b2c 74%,#8fae5a 100%)",
      glow: "radial-gradient(120% 90% at 50% 30%, rgba(143,174,90,.34), transparent 58%)",
      caption: "Brass in the wheat · SPREADING",
      img: "../../assets/art/scenes/clockwork-wheatfield.jpg",
      blurb: "A wheat field with brass gear growths, sick sky, wrong perspective. The wheat ticks like a metronome toward the horizon.",
      times: ["SPREADING phase only"],
      prompt: "wheat field with brass gear growths, sick sky, wrong perspective",
      corrupted: true,
      note: "Append corruption suffix: brass clockwork motifs in organic matter, sick green undertone."
    },
    {
      id: "edgewood_shrine", name: "Shrine of Unnamed Saints", kind: "Sacred",
      tint: "linear-gradient(165deg,#241d18 0%,#3c3024 44%,#5a4630 74%,#7c5c38 100%)",
      glow: "radial-gradient(80% 70% at 50% 70%, rgba(232,196,122,.32), transparent 60%)",
      caption: "Candle wall · the unfinished mural",
      blurb: "A shrine to saints nobody can name never lacks a candle. Its wall bears an incomplete mural \u2014 saints with missing faces, wheat threaded with brass, a road winding inward. Old women say finishing it would invite the road to arrive.",
      times: ["votive dusk", "empty noon"],
      prompt: "village shrine wall, incomplete mural, votive candles, faceless saints, brass-threaded wheat",
      note: "The mural gains a fragment each phase \u2014 corruption told through the wall, not the HUD."
    },
    {
      id: "hollow_hill", name: "Hollow Hill", kind: "Barrow",
      tint: "linear-gradient(165deg,#1c2420 0%,#2e3a30 46%,#46503e 76%,#5e6347 100%)",
      glow: "radial-gradient(110% 80% at 50% 86%, rgba(122,158,79,.16), transparent 60%)",
      caption: "Standing stones \u00b7 a door best left shut",
      img: "../../assets/art/scenes/forest-hidden-tunnel.jpg",
      blurb: "A hidden path off the game trails leads to barrows older than the village. Turf-roofed stone, a lintel worn smooth, dark beneath. Best left unopened until nerve and need align \u2014 the First Warden sleeps here, and not alone.",
      times: ["grey morning", "moonless"],
      prompt: "ancient turf-covered barrow mound, standing stones, dark stone doorway, mist",
      note: "Reachable only via a discovered hidden_path. Wrong-green seeps from the door at SPREADING+."
    },
    {
      id: "marches_road", name: "The Marches Road", kind: "Wrongness",
      tint: "linear-gradient(165deg,#20271c 0%,#37431f 44%,#5c6a2c 74%,#94b25c 100%)",
      glow: "radial-gradient(120% 90% at 50% 18%, rgba(143,174,90,.30), transparent 56%)",
      caption: "The road winding inward \u00b7 SPREADING",
      img: "../../assets/art/scenes/wheatfield-forest-edge.jpg",
      blurb: "The track that leaves Edgewood for the Heartlands. It took Odran an extra hour though the sun said otherwise. Milestones count down to a number that is not a distance. Walk it long enough and the wheat begins to stand in rows too straight for wind.",
      times: ["SPREADING phase only"],
      prompt: "frontier road winding toward distant wound of light, straight wheat rows, sick sky, wrong perspective",
      corrupted: true,
      note: "Milestones tick instead of measuring. The road is longer leaving than returning."
    },
    {
      id: "resting_camp", name: "The Roadside Camp", kind: "Wilds",
      tint: "linear-gradient(165deg,#231d16 0%,#39301f 44%,#5a4628 74%,#7c5e34 100%)",
      glow: "radial-gradient(70% 60% at 42% 64%, rgba(232,170,90,.36), transparent 60%)",
      caption: "Banked fire \u00b7 a night between roads",
      img: "../../assets/art/scenes/resting-camp.jpg",
      blurb: "A bedroll, a banked fire, a kettle going cold. Travelers rest here between the clearing and the gate \u2014 no inn, no walls, only the fire and whatever the dark brings to its edge. Stamina returns; nerve does not, always.",
      times: ["first watch", "grey dawn"],
      prompt: "roadside travelers' camp at night, bedroll, banked campfire, kettle, dark treeline",
      note: "Rest scene \u2014 stamina recovers. Encounters may interrupt at STIRRING+."
    },
    {
      id: "ruins_temple", name: "The Mage-Ruins", kind: "Ruins",
      tint: "linear-gradient(165deg,#1d2128 0%,#2f3640 46%,#4a4c4a 76%,#6a6356 100%)",
      glow: "radial-gradient(100% 78% at 50% 40%, rgba(190,118,58,.20), transparent 58%)",
      caption: "Broken colonnade \u00b7 older than the wound",
      img: "../../assets/art/scenes/ruins-temple-mages.jpg",
      blurb: "Toppled columns and a temple floor swallowed by root and moss. Whoever raised it knew the Clockwork Dark by an older name. Robed figures are carved into the stone \u2014 or were, once, standing where you stand now.",
      times: ["overcast", "storm-light"],
      prompt: "ruined temple colonnade, mossy broken columns, robed figures, grey storm light",
      note: "Lore-gate location. The carvings answer to ward pins."
    },
    {
      id: "clockwork_tower", name: "The Clockwork Tower", kind: "Wrongness",
      tint: "linear-gradient(165deg,#181b14 0%,#2c3318 46%,#4a5220 74%,#7c8a3a 100%)",
      glow: "radial-gradient(90% 80% at 50% 24%, rgba(143,174,90,.30), transparent 56%)",
      caption: "The heart of the wound \u00b7 CONSUMING",
      img: "../../assets/art/scenes/clockwork-tower.jpg",
      blurb: "Where the road has been counting toward. A spire of meshed brass and blackened stone rising from a field that ticks. The Clockwork Dark is not a demon you can banish \u2014 it is a logic, and this is where the logic keeps its time.",
      times: ["CONSUMING phase only"],
      prompt: "vast clockwork tower of brass gears and black stone, ticking wheat plain, bruised sky",
      corrupted: true,
      note: "End-state location. Visible on the horizon from SPREADING; reachable only at CONSUMING."
    },
  ],

  // ---------------------------------------------------------------
  // SOULS  (portrait 3:4, 768×1024)
  // ---------------------------------------------------------------
  npcs: [
    {
      id: "npc_maris", name: "Maris Hearth", role: "The Baker",
      tint: "linear-gradient(160deg,#3a2a1f 0%,#7a4f2a 55%,#d2a256 100%)",
      sil: "person", accent: "#e8c47a",
      mood: "Warmth with worry underneath",
      blurb: "Woman, 40s, flour on her forearms, kind tired eyes. She hums to keep the gears quiet and buys wild mushrooms from travelers.",
      prompt: "woman, 40s, flour on forearms, kind eyes, tired, bakery interior, oven glow",
      voice: "Soft maternal · flour in the voice"
    },
    {
      id: "npc_odran", name: "Odran Cartwright", role: "Caravan Master",
      tint: "linear-gradient(160deg,#2f2922 0%,#6b5236 55%,#b8863f 100%)",
      sil: "person", accent: "#c97a3c",
      mood: "Merchant cheer masking gossip hunger",
      blurb: "Man, 50s, weathered, a ledger always in hand, horse whip coiled at his belt. He trades twice a season and remembers every debt.",
      prompt: "man, 50s, weathered, ledger in hand, horse whip coiled, wagon trail at dusk",
      voice: "Merchant boom · brisk"
    },
    {
      id: "npc_ilya", name: "Ilya of the Nine Pins", role: "The Tinker",
      img: "../../assets/art/souls/tinker.jpg",
      tint: "linear-gradient(160deg,#33281f 0%,#7a5530 55%,#caa05a 100%)",
      sil: "person", accent: "#b8863f",
      mood: "Curious · a slightly unsettling smile",
      blurb: "Androgynous, sharp eyes, nine brass pins in the scarf. Sells sympathy charms and ward pins that sometimes work and sometimes merely reassure.",
      prompt: "androgynous, sharp eyes, nine brass pins in scarf, tent interior, hanging charms",
      voice: "Precise · careful",
      ambiguous: true
    },
    {
      id: "npc_sera", name: "Sergeant Sera Venn", role: "Militia",
      tint: "linear-gradient(160deg,#2a3036 0%,#4a565c 55%,#8a9088 100%)",
      sil: "person", accent: "#9aa0a0",
      mood: "Duty-heavy · not a villain",
      blurb: "Woman, 30s, a scar on her cheek, practical armor. She holds Millhaven gate in the rain while refugees thin the road behind her.",
      prompt: "woman, 30s, scar on cheek, practical armor, Millhaven gate, rain",
      voice: "Level · weary command"
    },
    {
      id: "npc_brindle", name: "Brindle", role: "Barn Cat · Assistant form",
      img: "../../assets/art/souls/cat-assistant.jpg",
      tint: "linear-gradient(160deg,#2c3a2a 0%,#4a4732 55%,#6e6a45 100%)",
      sil: "cat", accent: "#e8c47a",
      mood: "Cute, but uncanny",
      blurb: "A grey barn cat with too-knowing eyes and a curled tail. Sits at the village square's edge. The Assistant's earliest, lowest-trust face.",
      prompt: "grey barn cat, too-knowing eyes, tail curled, village square edge",
      voice: "— optional chime instead of voice",
      ambiguous: true
    },
    {
      id: "npc_greta", name: "Greta Moss", role: "The Shrine-keeper",
      tint: "linear-gradient(160deg,#2a241c 0%,#5a4a34 55%,#9a824e 100%)",
      sil: "person", accent: "#cbb07a",
      mood: "Piety thinned to warning",
      blurb: "Woman, 70s, votive wax on her knuckles and a saint's-bell at her belt. She tends the candles and refuses to finish the mural. She knew the road would change before the traders did, and she will not say how.",
      prompt: "old woman, 70s, votive wax on knuckles, shawl, shrine candlelight, faceless mural behind",
      voice: "Dry · scripture worn to plain warning"
    },
    {
      id: "npc_wren", name: "Wren", role: "The Gear-child",
      img: "../../assets/art/souls/child-assistant.jpg",
      tint: "linear-gradient(160deg,#26302a 0%,#46503c 55%,#6e6a48 100%)",
      sil: "child", accent: "#e8c47a",
      mood: "Draws what is coming",
      blurb: "A village child, maybe nine, charcoal on the fingers. Draws interlocking gears in the dirt of the square; by morning the drawings are gone. Says a quiet friend showed her how. Overlaps the Assistant's child form \u2014 nobody is certain which is which.",
      prompt: "child, 9, charcoal-stained fingers, drawing gears in dirt, village square dusk",
      voice: "Small · matter-of-fact about impossible things",
      ambiguous: true
    },
    {
      id: "npc_aldric", name: "Aldric Thorn", role: "The Woodcutter",
      tint: "linear-gradient(160deg,#222a20 0%,#3e4a32 55%,#6a6e48 100%)",
      sil: "person", accent: "#9aa06a",
      mood: "Practical · spooked by his own woods",
      blurb: "Man, 40s, axe over one shoulder, sawdust in his beard. He cuts the margin timber and knows which trails double back. Lately he will not work past the third birch \u2014 the game trails, he says, have started watching him back.",
      prompt: "woodcutter, 40s, axe on shoulder, sawdust beard, forest margin, long shadows",
      voice: "Blunt · fewer words after dark"
    },
  ],

  // Player archetypes — silhouette, not class
  archetypes: [
    { id: "wayfarer", name: "Wayfarer", gear: "Cloak, staff, road boots", look: "Travel-worn, practical", tint: "linear-gradient(160deg,#2c3a2a,#5a6a4a)" },
    { id: "hearthkeeper", name: "Hearthkeeper", gear: "Apron, rolled sleeves", look: "Flour dust, warm colors", tint: "linear-gradient(160deg,#5a3a22,#c79a4a)" },
    { id: "tinker", name: "Tinker-apprentice", gear: "Tool belt, goggles", look: "Brass pins, chalk stains", tint: "linear-gradient(160deg,#3a2f24,#a9683a)" },
  ],

  // ---------------------------------------------------------------
  // BESTIARY — rare, minimal combat. No raid bosses, no glow.
  // ---------------------------------------------------------------
  bestiary: [
    { id: "wolf", name: "Forest wolf", threat: "Hungry, not evil", when: "Any phase · birch dusk",
      img: "../../assets/art/enemies/wolf.jpg",
      blurb: "Lean and rain-wet, ribs showing. The honest danger of the margin — it wants the meat in your pack, not your soul. Flee is a real option." },
    { id: "deserter", name: "Militia deserter", threat: "Desperate human", when: "STIRRING · the wet road",
      img: "../../assets/art/souls/warrior.jpg",
      blurb: "A man who left Millhaven's gate before it shut. Mud, a notched blade, eyes that already lost. He is not a monster — which is the worst of it." },
    { id: "scarecrow", name: "Field scarecrow", threat: "Wrong, standing too still", when: "STIRRING · wheat margin",
      img: "../../assets/art/enemies/scarecrow.jpg",
      blurb: "It was a scarecrow yesterday. Today it faces the road, and nobody turned it. The first thing the wheat-corruption wears." },
    { id: "scarecrow_brass", name: "Corrupted scarecrow", threat: "Brass nails, wrong shadow", when: "SPREADING",
      img: "../../assets/art/enemies/scarecrow-clockwork.jpg",
      blurb: "Brass driven where straw should be, a shadow that falls the wrong way. It ticks. When it moves you wish it had stayed a scarecrow.", corrupted: true },
    { id: "clockwork_beast", name: "Clockwork beast", threat: "Gears in muscle", when: "SPREADING · the border",
      img: "../../assets/art/enemies/clockwork-monster-vs-mage.jpg",
      blurb: "Something that was an animal, rebuilt by the logic into a thing of meshed brass and meat. It does not hunger. It only continues.", corrupted: true },
    { id: "husk", name: "Clockwork husk", threat: "A clock where the heart was", when: "CONSUMING only",
      img: "../../assets/art/souls/clockwork-mage.jpg",
      blurb: "Brass ribs, linen tear, a stopped watch where the heart should beat. Not a raid boss — a person the Clockwork Dark finished with. It keeps the wrong hour.", corrupted: true },
  ],

  // ---------------------------------------------------------------
  // THE ASSISTANT — five canonical forms + the robed wizard study
  // ---------------------------------------------------------------
  assistantForms: [
    { form: "cat", when: "Early game · low trust", note: "Brindle, or a strange stray", sil: "cat", robe: "#5a6a4a", img: "../../assets/art/souls/cat-assistant.jpg" },
    { form: "wanderer", when: "Whisper arc", note: "Grey cloak, face in shadow", sil: "hood", robe: "#6a6e6a", img: "../../assets/art/souls/assistant-mage.jpg" },
    { form: "child", when: "STIRRING anomalies", note: "Draws gears in the dirt", sil: "child", robe: "#8a7a5a", img: "../../assets/art/souls/child-assistant.jpg" },
    { form: "tinker", when: "Trade / knowledge", note: "Overlaps Ilya — ambiguous", sil: "hood", robe: "#a9683a", img: "../../assets/art/souls/tinker.jpg" },
    { form: "reflection", when: "High Awareness", note: "Player silhouette in water", sil: "mirror", robe: "#4a565c", img: "../../assets/art/souls/shadow-mage-assistant.jpg" },
  ],

  // The robed wizard assistant — color study. The Assistant grows from
  // a cat into a hooded figure; the robe color reads its intent.
  robes: [
    { key: "white", name: "White Robe", hex: "#e9e2cd", trim: "#c7b98e", ink: "#3a3326",
      reads: "Mercy / the guide it pretends to be", phase: "DORMANT",
      blurb: "Linen-pale, almost saintly. The Assistant at its most reassuring — and least trustworthy. Bright until the line lands wrong." },
    { key: "grey", name: "Grey Robe", hex: "#6a6e6a", trim: "#4a4e4a", ink: "#e9e2cd",
      reads: "The wanderer · neutral, watching", phase: "STIRRING",
      blurb: "Road-dust grey, face in shadow. The whisper-arc form: dry, tired, pausing mid-sentence. It knows the road changed before you did." },
    { key: "red", name: "Red Robe", hex: "#7a2f2a", trim: "#5a201d", ink: "#f2e8d5",
      reads: "Appetite / the gears beneath",  phase: "SPREADING",
      blurb: "Quiet blood, not heraldry. Worn when the Assistant's interest sharpens into hunger. Brass threads catch the firelight at the hem." },
    { key: "black", name: "Black Robe", hex: "#1b1b18", trim: "#3a3a30", ink: "#d9b25f",
      reads: "The Clockwork Dark itself", phase: "CONSUMING",
      blurb: "Ironwood black, clockwork filigree at the cuffs. The form it wears when ambiguity is over. Candlelight makes the gears move." },
  ],

  // ---------------------------------------------------------------
  // THINGS  (item_icon 1:1, 256×256, flat illustrative)
  // ---------------------------------------------------------------
  items: [
    { name: "Loaf of bread", tag: "Food", price: "2c", from: "Maris", tint: "#c79a4a", seed: "rustic dark loaf of bread, flour dusted", img: "../../assets/art/things/bread.png" },
    { name: "Festival cake", tag: "Food", price: "8c", from: "Maris", tint: "#d8a85a", seed: "honey festival cake, dried fruit", img: "../../assets/art/things/steaming-bread.jpg" },
    { name: "Wild mushroom", tag: "Forage", price: "1c", from: "Forage", tint: "#8a6b4a", seed: "cluster of wild forest mushrooms", img: "../../assets/art/things/mushrooms.jpg" },
    { name: "Resin", tag: "Forage", price: "1c", from: "Forage", tint: "#a9683a", seed: "amber tree resin lump" },
    { name: "Wild herbs", tag: "Forage", price: "1c", from: "Forage", tint: "#6b7f5e", seed: "bundle of dried green herbs, twine", img: "../../assets/art/things/herbs.jpg" },
    { name: "River clay", tag: "Material", price: "1c", from: "Forage", tint: "#7a6a52", seed: "grey river clay lump" },
    { name: "Whetstone", tag: "Tool", price: "5c", from: "Odran", tint: "#5a5a57", seed: "worn rectangular whetstone", img: "../../assets/art/things/whetstone.jpg" },
    { name: "Road map to Millhaven", tag: "Knowledge", price: "15c", from: "Odran", tint: "#cbbf9a", seed: "hand-drawn road map, creased parchment", img: "../../assets/art/things/map.jpg" },
    { name: "Tinker knowledge map", tag: "Knowledge", price: "20c", from: "Ilya", tint: "#caa05a", seed: "chalk-marked map, brass pins, shifting roads", img: "../../assets/art/things/map.jpg" },
    { name: "Sympathy charm", tag: "Ward", price: "25c", from: "Ilya", tint: "#b8863f", seed: "brass sympathy charm on cord", brass: true, img: "../../assets/art/things/talisman.jpg" },
    { name: "Ward pin", tag: "Ward", price: "6c", from: "Ilya", tint: "#a9683a", seed: "small brass ward pin", brass: true, img: "../../assets/art/things/talisman-2.png" },
    { name: "Sympathy lamp", tag: "Ward", price: "—", from: "Ilya", tint: "#caa05a", seed: "small lamp burning a flame you cannot name", brass: true },
    { name: "Tallow candle", tag: "Light", price: "1c", from: "Maris", tint: "#e8c47a", seed: "stub of tallow candle, warm flame", img: "../../assets/art/things/candle-stack.jpg" },
    { name: "Travel cloak", tag: "Apparel", price: "12c", from: "Odran", tint: "#4a553d", seed: "road-worn wool travel cloak" },
    { name: "Iron ladle", tag: "Tool", price: "3c", from: "Maris", tint: "#5a5a57", seed: "iron bakery ladle" },
    { name: "Mushroom pottage", tag: "Craft", price: "—", from: "Recipe", tint: "#7a7048", seed: "bowl of mushroom pottage, steam" },
    { name: "Wax-sealed letter", tag: "Quest", price: "—", from: "Notice board", tint: "#cbbf9a", seed: "wax-sealed letter, militia seal" },
    { name: "Brass tooth", tag: "Wrong", price: "—", from: "Found", tint: "#8a7a3a", seed: "single brass tooth, uncanny", brass: true, corrupted: true },
    { name: "Gear-threaded wheat", tag: "Wrong", price: "—", from: "Border", tint: "#8fae5a", seed: "wheat stalk threaded with tiny brass gears", brass: true, corrupted: true },
    { name: "Child's gear drawing", tag: "Wrong", price: "—", from: "STIRRING", tint: "#9a8f6a", seed: "child's charcoal drawing of interlocking gears", corrupted: true },
    { name: "Wild berry", tag: "Forage", price: "1c", from: "Forage", tint: "#6b3a44", seed: "cluster of dark forest berries on the stem" },
    { name: "Honeycomb", tag: "Food", price: "2c", from: "Forage", tint: "#d8a85a", seed: "broken honeycomb dripping, wax cells" },
    { name: "Goat milk", tag: "Food", price: "1c", from: "Village", tint: "#cbbf9a", seed: "clay jug of fresh goat milk" },
    { name: "Saint's candle", tag: "Light", price: "1c", from: "Shrine", tint: "#e8c47a", seed: "votive candle, wax-run stub, faint flame" },
    { name: "Harvest lantern", tag: "Light", price: "4c", from: "Festival", tint: "#d6a24a", seed: "punched-tin harvest festival lantern, warm glow" },
    { name: "Ward bell", tag: "Ward", price: "9c", from: "Ilya", tint: "#b8863f", seed: "small brass hand-bell, ward sigil cast in the rim", brass: true, img: "../../assets/art/things/rune-talisman.jpg" },
    { name: "Brass filings", tag: "Wrong", price: "—", from: "Found", tint: "#8a7a3a", seed: "pinch of fine brass filings where teeth should be", brass: true, corrupted: true },
    { name: "Ringing loaf", tag: "Wrong", price: "—", from: "Bakery", tint: "#b08a44", seed: "split loaf of bread, brass glint in the crumb", corrupted: true, img: "../../assets/art/things/golden-ring-in-bread.jpg" },
    { name: "Old clock part", tag: "Wrong", price: "—", from: "Found", tint: "#7a6a3a", seed: "corroded brass clock gear, teeth worn uneven", brass: true, corrupted: true },
    { name: "Iron knife", tag: "Arms", price: "7c", from: "Odran", tint: "#6a6a66", seed: "forged iron belt knife, leather grip", img: "../../assets/art/things/iron-knife.jpg" },
    { name: "Stone knife", tag: "Arms", price: "2c", from: "Forage", tint: "#7a7068", seed: "knapped stone blade, cord-wrapped haft", img: "../../assets/art/things/stone-knife.png" },
    { name: "Wooden buckler", tag: "Arms", price: "10c", from: "Odran", tint: "#6b4a2a", seed: "round wooden buckler, iron boss, worn rim", img: "../../assets/art/things/wooden-shield.jpg" },
    { name: "Banded shield", tag: "Arms", price: "18c", from: "Millhaven", tint: "#5a4a36", seed: "small iron-banded shield, militia issue", img: "../../assets/art/things/small-shield.png" },
    { name: "Healing poultice", tag: "Heal", price: "4c", from: "Recipe", tint: "#7a8a5e", seed: "linen bandage and green yarrow poultice", img: "../../assets/art/things/bandage-poultice.png" },
    { name: "Yarrow draught", tag: "Heal", price: "6c", from: "Recipe", tint: "#6b5a3a", seed: "corked draught of herb tincture", img: "../../assets/art/things/potion.jpg" },
    { name: "Iron key", tag: "Quest", price: "—", from: "Found", tint: "#5a5a57", seed: "old iron key, teeth worn, ribbon tied", img: "../../assets/art/things/iron-key.jpg" },
    { name: "Copper coins", tag: "Coin", price: "—", from: "Currency", tint: "#b07a3a", seed: "small stack of copper coins, worn faces", img: "../../assets/art/things/coins.jpg" },
    { name: "Bone dice", tag: "Coin", price: "3c", from: "Odran", tint: "#cbbf9a", seed: "pair of bone dice and a wooden fate rune", img: "../../assets/art/things/dice-rune.png" },
  ],

  // ---------------------------------------------------------------
  // RUMORS (notice-board chatter) + MURAL fragments (the shrine wall)
  // ---------------------------------------------------------------
  rumors: [
    { text: "Odran swears the road to Millhaven took an extra hour though the sun said otherwise.", phase: "stirring" },
    { text: "A stillborn lamb was found with brass filings where its teeth should be.", phase: "spreading" },
    { text: "Maris burned a batch of bread that rang like a bell when it cracked.", phase: "stirring" },
    { text: "Tinkers are buying old clock parts at twice their weight in copper.", phase: "stirring" },
    { text: "The militia recruitment board has fresh nails \u2014 someone expects volunteers.", phase: "dormant" },
    { text: "Wheat near the corruption border stands in rows too straight for wind.", phase: "spreading" },
    { text: "Children in the square drew gears in the dirt; by morning the drawings were gone.", phase: "stirring" },
  ],

  // The unfinished mural \u2014 a fragment surfaces as each phase deepens.
  mural: [
    { frag: "a saint with clock-hands where eyes should be", phase: "dormant" },
    { frag: "wheat stalks threaded through brass gears", phase: "stirring" },
    { frag: "a child offering bread to something underground", phase: "stirring" },
    { frag: "the Marches road winding into a wound of light", phase: "spreading" },
    { frag: "a village burning in perfect symmetry", phase: "consuming" },
  ],

  // ---------------------------------------------------------------
  // WEATHER + PHASES (footer + image modifier)
  // ---------------------------------------------------------------
  weather: [
    { key: "clear", label: "Clear", note: "Honest light" },
    { key: "overcast", label: "Overcast", note: "Default mood" },
    { key: "mist", label: "Mist", note: "Forest margin" },
    { key: "rain", label: "Rain", note: "Millhaven" },
    { key: "wrong_rain", label: "Wrong rain", note: "Falls upward · STIRRING+", corrupted: true },
  ],

  phases: [
    { key: "dormant", label: "Dormant", mood: "Warm linen, moss, honey light", ui: "Clean journal; no corruption motifs" },
    { key: "stirring", label: "Stirring", mood: "Brass accents; shadows too long", ui: "Subtle tick motif in dividers" },
    { key: "spreading", label: "Spreading", mood: "Desaturated greens; sickly chartreuse", ui: "Weather widget shows wrong readings" },
    { key: "consuming", label: "Consuming", mood: "High contrast; clockwork filigree", ui: "Letterbox cutscenes; UI stutters 1 frame/min" },
  ],
};
