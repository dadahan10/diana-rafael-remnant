# -*- coding: utf-8 -*-
"""collection.html (EN, source of truth) -> collection-he.html (Hebrew, RTL).
Run after every edit of collection.html:  python build_he.py
Prints any English text that has no translation yet, so nothing slips through untranslated."""
import re, io

SRC, DST = "collection.html", "collection-he.html"

T = {  # English -> Hebrew, exact strings as they appear in the markup
 "REMNANT, the 2026 engagement collection by Diana Rafael. Whole, not perfect.": "REMNANT, קולקציית האירוסין של דיאנה רפאל ל-2026. שלם, לא מושלם.",
 "For a star to be born, there is one thing that must happen:": "כדי שכוכב ייוולד, דבר אחד חייב לקרות:",
 "a gaseous nebula must collapse.": "ערפילית של גז חייבת לקרוס.",
 "So collapse. Crumble.<br>This is not your destruction.": "אז לקרוס. להתפורר.<br>זה לא החורבן שלך.",
 "This is <em>your birth</em>.": "זו <em>הלידה שלך</em>.",
 "New Collection by Diana Rafael": "קולקציה חדשה מאת דיאנה רפאל",
 "The Story": "הסיפור",
 "What remains, <em>becomes</em>.": "מה שנשאר, <em>נהיה</em>.",
 "REMNANT was born from a personal chapter of breaking and loss. What came after was not a return to how things were. It was the slow work of gathering the pieces and joining them into something whole again: not perfect, newer than before, and still carrying its scars and the stories they tell.":
 "REMNANT נולדה מפרק אישי של שבר ואובדן. מה שבא אחריו לא היה חזרה למה שהיה. זו הייתה עבודה איטית של איסוף החתיכות וחיבורן למשהו שלם מחדש: לא מושלם, חדש יותר מבעבר, ועדיין נושא את הצלקות שלו ואת הסיפורים שהן מספרות.",
 "That is the collection. Every piece holds a fracture that was not hidden, but made the point.": "זו הקולקציה. בכל תכשיט יש שבר שלא הוסתר, אלא הפך לעיקר.",
 "The wound is where the light enters.": "הפצע הוא המקום שדרכו נכנס האור.",
 "There is a crack in everything. That's how the light gets in.": "בכל דבר יש סדק. ככה האור נכנס.",
 "Kintsugi": "קינצוגי",
 "Repaired <em>in gold</em>.": "מתוקן <em>בזהב</em>.",
 "The break is not concealed. It becomes the most precious line in the object.": "השבר לא מוסתר. הוא הופך לקו היקר ביותר בחפץ.",
 "The Japanese art of mending broken ceramics with gold. A bowl that shattered is not thrown away and not disguised. Its seams are filled with gold, so that the history of the break is the first thing you see, and the most beautiful.":
 "אמנות יפנית של איחוי קרמיקה שבורה בזהב. קערה שהתנפצה לא נזרקת ולא מוסווית. התפרים שלה מתמלאים זהב, כך שההיסטוריה של השבר היא הדבר הראשון שרואים, והיפה ביותר.",
 "That is how we think about every piece in REMNANT. The fracture is the design.": "ככה אנחנו חושבים על כל תכשיט ב-REMNANT. השבר הוא העיצוב.",
 "You need chaos in you to give birth to a dancing star.": "צריך כאוס בתוכך כדי ללדת כוכב רוקד.",
 "Supernova": "סופרנובה",
 "A star that <em>collapses</em>.": "כוכב <em>שקורס</em>.",
 "The end of one thing is the raw material of the next.": "הסוף של דבר אחד הוא חומר הגלם של הבא אחריו.",
 "When a star can no longer hold itself together, it collapses and explodes. Its matter is thrown across space. And over time, that scattered matter gathers again, pulled together by its own gravity, into a new star, a new world.":
 "כשכוכב כבר לא מסוגל להחזיק את עצמו, הוא קורס ומתפוצץ. החומר שלו נזרק לרחבי החלל. ועם הזמן, החומר המפוזר הזה מתאסף שוב, נמשך יחד בכוח הכבידה של עצמו, לכוכב חדש, לעולם חדש.",
 "What remains after the explosion is what the next thing is made of. The collection takes its name from this.": "מה שנשאר אחרי ההתפוצצות הוא מה שממנו עשוי הדבר הבא. מכאן הקולקציה לקחה את שמה.",
 "The phoenix must burn to emerge.": "עוף החול חייב לבעור כדי לקום.",
 "Solar wind": "רוח שמש",
 "Particles that <em>give life</em>.": "חלקיקים <em>שנותנים חיים</em>.",
 "What looks like violence is also what carries the ingredients of life.": "מה שנראה כאלימות הוא גם מה שנושא את מרכיבי החיים.",
 "Eruptions on the surface of a sun send streams of particles out across its whole system. On a planet far away they light up the sky, and they carry with them the elements that life is built from.":
 "התפרצויות על פני השמש שולחות זרמים של חלקיקים אל כל המערכת שלה. על כוכב לכת רחוק הם מאירים את השמיים, ונושאים איתם את היסודות שמהם בנויים החיים.",
 "The rays of Sunburst and the drifting stones of Formation come from here: something leaving its center, and arriving somewhere as light.": "הקרניים של Sunburst והאבנים הנודדות של Formation באות מכאן: משהו שעוזב את המרכז שלו, ומגיע למקום אחר כאור.",
 "Behind every beautiful thing, some kind of pain.": "מאחורי כל דבר יפה, כאב כלשהו.",
 "Craquelure": "קראקלור",
 "A map <em>of cracks</em>.": "מפה <em>של סדקים</em>.",
 "Each line is a moment of stress that held.": "כל קו הוא רגע של לחץ שהחזיק מעמד.",
 "On a painting five hundred years old, time draws a fine web of cracks across the surface. None of them broke the picture. Together they are a record of everything it went through, and they are what make an old masterpiece impossible to fake.":
 "על ציור בן חמש מאות שנה, הזמן מצייר רשת עדינה של סדקים על פני השטח. אף אחד מהם לא שבר את התמונה. יחד הם תיעוד של כל מה שהיא עברה, והם מה שהופך יצירת מופת עתיקה לבלתי אפשרית לזיוף.",
 "Craquelere, the sixth design, wears that web across a wide blade of gold.": "Craquelere, העיצוב השישי, לובש את הרשת הזו על להב רחב של זהב.",
 "What the collection stands for": "מה שהקולקציה מאמינה בו",
 "Whole, <em>not perfect</em>.": "שלם, <em>לא מושלם</em>.",
 "Whole,<span>not perfect</span>": "שלם,<span>לא מושלם</span>",
 "The seam shows. That is the point.": "התפר נראה. זו הנקודה.",
 "Rising<span>again</span>": "לקום<span>מחדש</span>",
 "Made after the fall, not in spite of it.": "נעשה אחרי הנפילה, לא למרות הנפילה.",
 "Endurance<span>that lasts</span>": "עמידות<span>לאורך זמן</span>",
 "Solid gold and real stones, built to be worn every day for a lifetime.": "זהב מלא ואבנים אמיתיות, בנויים להילבש כל יום, לכל החיים.",
 "Inner<span>strength</span>": "כוח<span>פנימי</span>",
 "Dark diamonds, quiet forms. Nothing needs to shout.": "יהלומים כהים, צורות שקטות. שום דבר לא צריך לצעוק.",
 "You are not the darkness you endured. You are the light that refused to give up.": "לא החושך שעברת. האור שסירב לכבות.",
 "The Designs": "העיצובים",
 "Ten stories, <em>three ways</em> each.": "עשרה סיפורים, <em>בשלוש דרכים</em>.",
 "Every design is made as an engagement ring, a wedding band, and a pair of earrings.": "כל עיצוב נעשה כטבעת אירוסין, כטבעת נישואין וכזוג עגילים.",
 "A time to break, a time to build.": "עת לפרוץ ועת לבנות.",
 "A signet form with two rails circling the stone. The wave rises at the top and settles as it travels around the finger.": "צורת חותם עם שני מסלולים שמקיפים את האבן. הגל עולה למעלה ונרגע כשהוא נע סביב האצבע.",
 "Black side diamonds in rose gold. Scattered particles drawn toward each other, settling into something new.": "יהלומי צד שחורים בזהב אדום. חלקיקים מפוזרים שנמשכים זה לזה ומתיישבים למשהו חדש.",
 "A black disc in rose gold holding a white diamond at its center. Matter spinning inward until it becomes one.": "דיסק שחור בזהב אדום שמחזיק יהלום לבן במרכזו. חומר שמסתובב פנימה עד שהוא נהיה אחד.",
 "A black marquise on a scarred blade of yellow gold. The surface keeps the marks of what it went through.": "מרקיזה שחורה על להב מצולק של זהב צהוב. פני השטח שומרים את הסימנים של מה שעבר.",
 "A dark oval on a softly rounded blade of rose gold. Edges worn smooth by time, the way a river shapes stone.": "אובל כהה על להב מעוגל ורך של זהב אדום. קצוות שהזמן שחק, כמו נהר שמעצב אבן.",
 "A wide blade covered in a crackle pattern, like the glaze of an old ceramic. A whole made of many held cracks.": "להב רחב מכוסה בדוגמת סדקים, כמו זיגוג של קרמיקה עתיקה. שלם שעשוי מהרבה סדקים שהחזיקו מעמד.",
 "A wide pale band with lines of gold breaking through it. The repair is the design.": "פס רחב ובהיר עם קווי זהב שפורצים דרכו. התיקון הוא העיצוב.",
 "A smooth band with stars cut straight through the metal. Light passes where the gold is missing.": "פס חלק עם כוכבים חתוכים ישר דרך המתכת. האור עובר במקום שבו הזהב חסר.",
 "A band carrying a web inside it, the way galaxies hang on invisible threads across the universe.": "פס שנושא בתוכו רשת, כמו גלקסיות שתלויות על חוטים בלתי נראים לרוחב היקום.",
 "Rays leaving a single point, with small circles at their ends. The eruption that sends light outward.": "קרניים שיוצאות מנקודה אחת, עם עיגולים קטנים בקצותיהן. ההתפרצות ששולחת אור החוצה.",
 ">Engagement<": ">אירוסין<", ">Wedding band<": ">טבעת נישואין<", ">Earrings<": ">עגילים<",
 "Every piece is made to order, by hand. When you write to us, you'll always get a real person, never an AI. That's a promise.":
 "כל תכשיט נעשה בהזמנה אישית, בעבודת יד. כשכותבים לנו, תמיד עונה בן אדם אמיתי, לעולם לא AI. זו הבטחה.",
 "REMNANT · Engagement &amp; Wedding Collection · 2026": "REMNANT · קולקציית אירוסין ונישואין · 2026",
 "Kintsugi photo: Wikimedia Commons, CC BY-SA 4.0 · Solar image: NASA/SDO": "צילום קינצוגי: Wikimedia Commons, CC BY-SA 4.0 · צילום השמש: NASA/SDO",
 '<a class="lang" href="collection-he.html">עברית</a>': '<a class="lang" href="collection.html">English</a>',
}
for i in range(1, 11):
    T[f">No. {i}<"] = f">מס׳ {i}<"

CSS = [  # RTL + Hebrew typography
 ("<html lang=\"en\">", "<html lang=\"he\" dir=\"rtl\">"),
 ("family=Montserrat:wght@200;300;400&display=swap", "family=Montserrat:wght@200;300;400&family=Frank+Ruhl+Libre:wght@300;400&family=Assistant:wght@200;300;400&display=swap"),
 ("body { background:var(--black); color:var(--bone); font-family:'Cormorant Garamond',serif;", "body { background:var(--black); color:var(--bone); font-family:'Frank Ruhl Libre','Cormorant Garamond',serif;"),
 ("</style>", "  /* Hebrew overrides (must come last) */\n  .title, .design h3, .num { font-family:'Cormorant Garamond',serif; }\n  .label, .sub, .k, .no, .cap, .by, footer a, footer .fine { letter-spacing:.12em !important; }\n  .label, .k, .no, .by, footer .fine { font-size:.8rem !important; }\n  .cap { font-size:.7rem !important; }\n  .by { direction:ltr; }\n  .lang { right:auto; left:1rem; }\n</style>"),
 ("font-family:'Montserrat',sans-serif", "font-family:'Assistant','Montserrat',sans-serif"),
 ("border-left:1px solid var(--gold); padding-left:1rem;", "border-right:1px solid var(--gold); padding-right:1rem;"),
 ("float:left; line-height:.8; padding:.1em .12em 0 0;", "float:right; line-height:.8; padding:.1em 0 0 .12em;"),
 ("padding-left:.9rem; border-left:1px solid rgba(201,168,76,.5);", "padding-right:.9rem; border-right:1px solid rgba(201,168,76,.5);"),
 ("padding-left:1rem; border-left:1px solid rgba(201,168,76,.5);", "padding-right:1rem; border-right:1px solid rgba(201,168,76,.5);"),
]

html = io.open(SRC, encoding="utf-8").read()
for a, b in CSS:
    assert a in html, "CSS anchor missing: " + a[:50]
    html = html.replace(a, b)
for a in sorted(T, key=len, reverse=True):
    html = html.replace(a, T[a])
io.open(DST, "w", encoding="utf-8").write(html)

# report untranslated visible text (Latin words outside tags/script/style), ignoring brand/design names
body = re.sub(r"<(script|style).*?</\1>", "", html[html.find("<body"):], flags=re.S)
texts = [t.strip() for t in re.sub(r"<[^>]+>", "\n", body).splitlines() if t.strip()]
ok = {"Remnant", "Diana Rafael", "dianarafael.com", "— r.h. sin", "English", "Gravitational Wave", "Formation", "Accretion",
      "Disturbed", "Smoothen", "Craquelere", "Kintsugi", "Starz", "Cosmic Web", "Sunburst"}
left = [t for t in texts if re.search(r"[A-Za-z]{3,}", t) and t not in ok and not re.search(r"[֐-׿]", t)]
print("written", DST, "| untranslated:", left or "none")
