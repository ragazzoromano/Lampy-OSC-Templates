"""Basic checks for TouchOSC .tosc layout files.

Usage: python3 scripts/validate_tosc.py templates/*.tosc

A .tosc file is zlib-compressed XML. For every file this script checks that:
  * it decompresses and parses as XML
  * every control has a unique ID
  * every control lies inside its page
  * every OSC message that is sent uses a /lampy/... address
Exits with status 1 if any check fails.
"""
import glob
import sys
import zlib
import xml.etree.ElementTree as ET


def prop(node, key):
    props = node.find("properties")
    if props is None:
        return None
    for p in props:
        if p.find("key").text == key:
            return p.find("value")
    return None


def frame(node):
    f = prop(node, "frame")
    return [float(f.find(c).text) for c in "xywh"]


def osc_path(osc):
    return "".join(p.find("value").text or "" for p in osc.find("path"))


def check(path):
    errors = []
    try:
        root = ET.fromstring(zlib.decompress(open(path, "rb").read()))
    except Exception as exc:  # noqa: BLE001 - report any read/parse failure
        return [f"cannot read: {exc}"]

    ids = [n.get("ID") for n in root.iter("node")]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        errors.append(f"{len(dupes)} duplicate control IDs")

    pager = root.find("node/children/node")
    if pager is None or pager.get("type") != "PAGER":
        errors.append("no pager found under the root group")
        pages = []
    else:
        pages = pager.find("children").findall("node")
    for page in pages:
        label = prop(page, "tabLabel").text
        pw, ph = frame(page)[2:]
        for n in page.find("children").findall("node"):
            x, y, w, h = frame(n)
            if x < 0 or y < 0 or x + w > pw or y + h > ph:
                errors.append(f"page '{label}': '{prop(n, 'name').text}' is outside the page")

    for n in root.iter("node"):
        msgs = n.find("messages")
        if msgs is None:
            continue
        for osc in msgs.findall("osc"):
            if osc.find("send").text == "1":
                p = osc_path(osc)
                if not p.startswith("/lampy/"):
                    errors.append(f"'{prop(n, 'name').text}' sends non-LAMPY address '{p}'")

    print(f"{path}: {len(pages)} pages, {len(ids)} controls - {'OK' if not errors else 'FAILED'}")
    return errors


def main(args):
    # Windows shells don't expand wildcards, so expand them here.
    paths = [p for a in args for p in (sorted(glob.glob(a)) or [a])]
    if not paths:
        print(__doc__)
        return 2
    failed = False
    for path in paths:
        for err in check(path):
            failed = True
            print(f"  ERROR {err}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
