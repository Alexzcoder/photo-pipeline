# Prompt builder for carpet marketing shots. Shared with the studio web tool; keep both copies identical.
# python prompts.py  -> self-check

STYLES = {
 "classic-oriental":  "warm traditional, walnut and dark wood furniture, classic upholstery",
 "modern-minimal":    "clean contemporary, pale walls, low-profile furniture",
 "vintage-distressed":"warm cozy vintage-styled, soft neutral tones, classic furniture",
 "art-deco":          "elegant art-deco, brass accents, velvet upholstery",
 "botanical":         "fresh airy, plants and rattan, linen textiles",
 "scandi-soft":       "soft scandinavian, white walls, pale wood, wool throws",
 "luxe-baroque":      "opulent classic interior, ornate mouldings, rich fabrics",
 "bold-contrast":     "striking modern, dark accent wall, sculptural furniture",
 "kids":              "cheerful children's room, playful pastel palette, soft toys and low furniture",
}
LIGHTS = {
 "daylight":   "bright soft natural daylight from large windows",
 "golden":     "warm late-afternoon golden-hour sunlight",
 "evening":    "cozy evening, warm lamplight and soft shadows",
 "overcast":   "soft diffused overcast daylight, even and shadowless",
}
# key: (label, room description, placement) — placement may be {"md":..., "lg":...} chosen by rug area
ROOMS = {
 "livingroom": ("Living room", "living room with a sofa, armchair and coffee table",
    {"md": "sits in front of the sofa under the coffee table with the sofa's front legs resting on it, plenty of bare floor around",
     "lg": "sits under the seating group with the sofa's front legs and the coffee table on it; the rug is only a little wider than the sofa"}),
 "bedroom":    ("Bedroom", "bedroom with a double bed",
    {"md": "runs along the side of the bed as a bedside rug, reaching from bedside table to the foot of the bed",
     "lg": "sits under the bed with most of the bed's length on it and generous rug showing on all sides"}),
 "dining":     ("Dining room", "dining room with a table and six chairs", "sits under the full dining set with the entire table and all chairs on the rug, a border of floor near the walls"),
 "entryway":   ("Entryway", "bright entrance hall", "lies along the hallway with a console table and a bench beside it, bare floor visible at both ends"),
 "office":     ("Home office", "home office", "sits under the desk and chair with the chair rolling on it, floor showing around the edges"),
 "readingnook":("Reading nook", "cozy reading corner by a window", "sits under an armchair, footstool and small side table, framed by bare floor"),
 "openplan":   ("Open plan", "open-plan living and dining space", "defines the seating zone with the sofa front legs and coffee table on it, plenty of plain floor visible beyond its edges"),
 "lounge":     ("Lounge", "lounge with a sectional sofa", "sits under the sectional's front edge and the coffee table, its far edge stopping well short of the walls"),
 "kitchen":    ("Kitchen", "modern kitchen with an island", "runs along the floor in front of the kitchen island as a runner, bare floor on both sides"),
 "kidsroom":   ("Kids room", "cheerful child's bedroom with a single bed", "covers the play area beside the bed with toys and a low bookshelf around it, bare floor near the walls"),
 "playroom":   ("Playroom", "bright playroom", "fills the centre of the room with a toy chest, bean bag and play table on it"),
 "nursery":    ("Nursery", "soft nursery", "sits in the middle of the room with a cot, changing table and rocking chair around its edges"),
}
SPECIAL = {"studio": "Studio flat", "rolled": "Rolled up"}
ORDER = ["studio"] + list(ROOMS) + ["rolled"]   # numbering order in output filenames

OVERLAY = (" NOTE: the reference photo has an advertising price banner pasted over its top-left corner and a "
           "small logo watermark top-right. These are overlays, not part of the rug - ignore them completely and "
           "reconstruct the rug pattern underneath so the rug reads whole and unobstructed. "
           "No text, logos, watermarks or banners anywhere in the output.")
STUDIO_BG = ("on a smooth clean pale floor inside a bright white seamless studio cyclorama backdrop that curves up behind it, "
             "soft even professional lighting, gentle soft contact shadow. Bright clean high-end furniture-brand catalogue look, "
             "NOT a warehouse or concrete floor.")

def build_prompts(w, l, scenes, style, light, banner):
    """Return {scene_key: prompt}. w,l in metres."""
    ov = OVERLAY if banner else ""
    short, long_ = min(w, l), max(w, l)
    cls = "md" if w * l <= 4.2 else "lg"
    keep = (f"Reproduce the rug's exact pattern, colours and proportions as in the reference photo. "
            f"CRITICAL SCALE: this rug is exactly {w} m x {l} m. A three-seat sofa is 2.1 m long and an interior door "
            f"0.8 m wide, so the rug's long side is about {long_/2.1:.1f} sofa-lengths and its short side about "
            f"{short/0.8:.1f} door-widths. Draw it at exactly that size against the furniture - no larger. "
            f"Show an ordinary home room of realistic proportions, not a grand hall, ballroom or showroom.")
    out = {}
    for key in ORDER:
        if key not in scenes: continue
        if key == "studio":
            out[key] = ("Professional e-commerce studio product photograph of this exact rug laid flat and fully visible, "
                        + STUDIO_BG + " Slight top-down angle. Reproduce the rug's exact pattern, colours and proportions "
                        "as in the reference photo. Photorealistic, high detail, no text." + ov)
        elif key == "rolled":
            out[key] = ("Professional e-commerce studio photograph of this exact rug partially rolled up from one short end, "
                        "about one third rolled, lying " + STUDIO_BG + " The roll is kept slim and tight with low interior volume. "
                        "The reverse underside of the rug and its bound edge seam are clearly visible on the rolled part, while the "
                        "rest lies flat showing the pattern. Reproduce the rug's exact pattern, colours and proportions as in the "
                        "reference. Photorealistic, no text." + ov)
        else:
            _, room, place = ROOMS[key]
            if isinstance(place, dict): place = place[cls]
            out[key] = (f"Photorealistic {STYLES[style]}, {LIGHTS[light]}, {room}. This exact rug (real size {w} x {l} metres) "
                        f"{place}. {keep} Professional interior photography, no text." + ov)
    return out

if __name__ == "__main__":
    p = build_prompts(1.6, 2.3, ["studio", "livingroom", "rolled"], "scandi-soft", "daylight", True)
    assert list(p) == ["studio", "livingroom", "rolled"]
    assert "1.1 sofa-lengths" in p["livingroom"] and "front legs resting" in p["livingroom"]
    assert "little wider than the sofa" in build_prompts(2, 3, ["livingroom"], "kids", "evening", False)["livingroom"]
    assert "price banner" in p["studio"]
    print("prompts ok")
