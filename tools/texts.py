"""Texts shared by the phone version (phone.py) and the desktop site (fromphone.py): drafts by Claude, 21 Oct 2026, for Steuart to adjust.
The closing line on contact is Steuart's wording."""

INFO_TXT = ('Building is a big step, and it helps to know what to expect. These short guides explain why it pays to work with an architect, '
            'how a project runs from first idea to finished building, what it costs and who takes part along the way. Have a look – then simply get in touch.')
LINKS_TXT = ('Useful addresses for anyone planning to build in Vienna or Austria: the chambers that register architects, '
             'the city offices for permits and building rules, and good places to see and learn more about architecture.')
CONTACT_TXT = '<i class="hd">–</i>Write, call or come visit us!<br>We’d be happy to discuss your project, large or small.<i class="hd">–</i>'   # Steuart's wording, 21 Oct
INTRO = ('<b class="dd">dasein-design</b> is a small architecture and design practice in Vienna, run as a partnership since 2003. '
         'We design homes, courtyards and interiors – and the furniture, exhibitions and graphics that go with them. '
         'We listen first, keep things simple and build for the people who will live with the result.')
BIO = ['Both partners studied at the Mackintosh School of Architecture in Glasgow and are registered architects in Austria (Ziviltechniker) and in the United Kingdom (ARB). '
       'Between them they have worked for practices in Vienna, London and Glasgow on everything from small conversions to large city buildings.',
       'Cuong Tran-Viet also studied at TU Wien and at the Bartlett in London, spent ten years with Aedas in London and nine with BEHF Architects in Vienna. '
       'Steuart Harrison taught design for fifteen years at TU Wien and for several years at New Design University St. Pölten.',
       'We work in German and English. The partners run every project themselves, from the first sketch to the last detail on site – '
       'for private clients, small businesses, communities and cultural institutions.']

# compact lines for the phone's OUR SERVICES box (drafts by Claude, from the Figma blocks)
SERVICES_SHORT = {'IT': 'Archicad, AutoCAD, Revit &amp; more',
                  'PROJEKTE': 'Vorentwurf bis Ausführung, örtl. Bauaufsicht',
                  'SKILLS': 'Möbeldesign, Wohnen, Ateliers, Ausstellungen'}
# the three service blocks from the desktop "us & our services" page (Figma text; SKILLS still repeats PROJEKTE there)
SERVICES = [('IT', 'ic-it.svg', ['Experte: Archicad',
             'gute Kenntnisse: AutoCAD, Microstation V8 &amp; Triforma, 3d Studio MAX+VRAY, Adobe Paket, Microsoft Office Paket, FormZ, Bentley Generative Components, Solibri Modelchecker, Vectorworks.',
             'Grundkenntnisse: Autodesk Revit, Rhinoceros, SidounWinAVA, NBS Building.']),
            ('PROJEKTE', 'ic-projekte.svg', ['Vorentwurf bis Ausführungsplanung, Möbeldesign, örtl. Bauaufsicht für diverse Projekte, darunter eine Hotel Pension, Kleingartenhäuser, Wohnungen, Klavierübungsstudio, Büro, Ausstellungen, Ateliers / Café-Bar &amp; Einfamilienhäuser hauptsächlich in Wien.']),
            ('SKILLS', 'ic-skills.svg', ['Vorentwurf bis Ausführungsplanung, Möbeldesign, örtl. Bauaufsicht für diverse Projekte, darunter eine Hotel Pension, Kleingartenhäuser, Wohnungen, Klavierübungsstudio, Büro, Ausstellungen, Ateliers / Café-Bar &amp; Einfamilienhäuser hauptsächlich in Wien.'])]

# the impressum (draft by Claude, 22 Oct 2026 - to be checked by the office / the ZT Kammer); shared by the phone page 06 and the desktop pop-up
LEGAL_BODY = ('<p class="lp">Informationen gemäß § 5 E-Commerce-Gesetz und Offenlegung gemäß § 25 Mediengesetz</p>'
         '<h4>Medieninhaber, Herausgeber und Diensteanbieter</h4>'
         '<p><b>Arch. DI Cuong TRAN-VIET</b><br>Architekt (Ziviltechniker) · Inhaber von <b class="dd">dasein-design</b><br>Neulerchenfelderstrasse 42/6 · A-1160 Wien · Österreich<br>'
         'T <a href="tel:+436764822464">+43 (0)676 4822 464</a> · E <a href="mailto:cuong@dasein-design.net">cuong@dasein-design.net</a></p>'
         '<h4>Unternehmensgegenstand</h4><p>Architektur, Planung und Design</p>'
         '<h4>Berufsbezeichnung und Kammer</h4><p>Architekt (Ziviltechniker), Berufsbezeichnung verliehen in Österreich.<br>'
         'Mitglied der Kammer der Ziviltechniker:innen für Wien, Niederösterreich und Burgenland (ZT Kammer Ost), Karlsgasse 9, 1040 Wien · <a href="https://ost.zt.at/">ost.zt.at</a></p>'
         '<h4>Berufsrecht</h4><p>Ziviltechnikergesetz 2019 (ZTG 2019) und Standesregeln der Ziviltechniker:innen, abrufbar unter <a href="https://www.ris.bka.gv.at/">www.ris.bka.gv.at</a> und <a href="https://ost.zt.at/">ost.zt.at</a></p>'
         '<h4>Aufsichtsbehörde</h4><p class="todo">[zuständiges Bundesministerium – bitte bestätigen]</p>'
         '<h4>UID-Nummer</h4><p class="todo">[ATU – bitte ergänzen]</p>'
         '<h4>Mitarbeit</h4><p><b>Steuart J Mackenzie HARRISON</b> BArch MArch ARB<br>Architect<br>Mitarbeit · Gestaltung dieser Website</p>'
         '<h4>Haftung und Urheberrecht</h4><p>Die Inhalte dieser Website wurden mit Sorgfalt erstellt; für Richtigkeit, Vollständigkeit und Aktualität wird keine Gewähr übernommen. '
         'Für die Inhalte verlinkter Websites sind ausschließlich deren Betreiber verantwortlich. Texte, Bilder und Pläne sind urheberrechtlich geschützt; '
         'jede Verwendung bedarf der vorherigen Zustimmung.</p>'
         '<h4>Datenschutz</h4><p>Diese Website setzt keine Cookies und speichert selbst keine personenbezogenen Daten. Die Website liegt bei GitHub Pages (GitHub Inc.); die Karte im Kontaktbereich wird von den Servern der OpenStreetMap Foundation geladen, die Kartensoftware Leaflet von cdnjs (Cloudflare). Beim Aufruf übermittelt Ihr Browser dabei technisch notwendig Ihre IP-Adresse an diese Anbieter. '
         '<span class="todo">[Datenschutzerklärung – bitte ergänzen]</span></p>')


# ---------- bits & bats (shared by phone and desktop, 22 Oct): photos (file, tall on the phone, caption), notes and links ----------
BITS = [('bits-imgImage.webp', 0, 'The DILLON Shelf Plans'), ('p-drawing-grille.webp', 1, 'dd - NEW LOGO &amp; IDENTITY'),
        ('p-pocket-watch.webp', 0, 'INTERIOR COURTYARDS'), ('p-barriers-night.webp', 0, 'MIRROR BALL &amp; DISCO HALLS'),
        ('p-cages-night.webp', 0, 'SKI SLOPES IN SUMMER'), ('bits-imgImage3.webp', 0, 'PAPPI IN THE MIRROR'),
        ('p-plastic-sheet.webp', 0, 'dd - OUR OLD LOGO'), ('p-section-grey.webp', 0, 'AIDA - THE BEST COFFEE CHAIN'),
        ('bits-imgImage6.webp', 0, 'PAINT IT BLACK'), ('bits-imgImage7.webp', 0, 'CAFE PRÜCKEL...THE GHOSTS OF'),
        ('p-scaffolding.webp', 1, 'Hr. KARL SCHWANZER'), ('bits-imgImage9.webp', 0, 'BOLLOCKS BOLLOCKS!...Goat*'),
        ('p-streaks-white-blue.webp', 1, 'dd - NEW BUSINESS CARDS'), ('bits-imgImage11.webp', 0, 'VERTICAL ACCESS or STAIRS'),
        ('p-tower-drawing-blue.webp', 0, 'MUSEUMS QUARTIER'), ('bits-imgImage13.webp', 0, 'MMEEELLLAAA'),
        ('bits-imgImage14.webp', 0, 'MEESHHHA'), ('bits-imgImage15.webp', 0, 'THE “DUDE” IN VENICE'),
        ('bits-imgImage16.webp', 0, 'A. N. HARKESS'), ('p-streaks-orange.webp', 0, 'LIGHT AT THE END OF THE TUNNEL'),
        ('p-akh-crate.webp', 1, 'WHO IS THIS GUY?'),
        # 22 Oct: more of Steuart's photos (some also appear in the project pop-ups)
        ('p-light-hole.webp', 0, 'LIGHT HOLE'), ('p-wasp-red.webp', 0, 'WASP ON RED'), ('p-yellow-dots-box.webp', 1, 'YELLOW DOTS'),
        ('p-carrots-plate.webp', 0, 'CARROTS, STRIPES'), ('p-milk-glass.webp', 0, 'MILK GLASS'), ('p-banana-tape.webp', 0, 'BANANA &amp; TAPE'),
        ('p-flower-shadows.webp', 0, 'FLOWER SHADOWS'), ('p-coffee-stain.webp', 0, 'COFFEE STAIN'), ('p-light-switch.webp', 0, 'LIGHT SWITCH'),
        ('p-paper-shreds.webp', 1, 'PAPER SHREDS'), ('p-horse-rider.webp', 0, 'HORSE &amp; RIDER'), ('p-torn-strips-photo.webp', 0, 'TORN STRIPS')]
# notes and links between the photos - a looser, blog-like mix (drafts by Claude, 22 Oct; the articles are real, checked that day)
CARDS = [('note', 'Otto Wagner, Moderne Architektur, 1896', '„Etwas Unpraktisches kann nicht schön sein.“',
          '„Etwas Unpraktisches kann nicht schön sein.“<br><br>Otto Wagner wrote this in Vienna in 1896, in <i>Moderne Architektur</i> – a sentence we still pin above the drawing board.', ''),
         ('news', 'archiweb', 'A timber museum for the MuseumsQuartier',
          'The House of Austrian History (hdgö) moves to the MuseumsQuartier in 2028, with a new timber entrance building by O&amp;O Baukunst – construction is due to start in the second half of 2026.',
          'https://www.archiweb.cz/en/n/foreign/ve-vidni-postavi-muzeum-dejin-rakouska-jako-moderni-drevostavbu'),
         ('note', 'studio note', 'Start with a walk.',
          'Every project starts with a walk round the site, a sketchbook and a lot of questions – where the light comes from, what the neighbours see, what should stay. <span class="todo">[draft – Steuart to write]</span>', ''),
         ('news', 'vienna.at', 'Open House Wien: 53 buildings open their doors',
          'The eleventh Open House Wien opened 53 otherwise closed buildings and spaces across Vienna for free, on the theme of adapting architecture to climate and social change.',
          'https://www.vienna.at/open-house-vienna-opens-53-otherwise-closed-buildings/10369079'),
         ('note', 'Adolf Loos, Ornament und Verbrechen, 1908', '„Die Evolution der Kultur ist gleichbedeutend mit dem Entfernen des Ornamentes aus dem Gebrauchsgegenstande.“',
          '„Die Evolution der Kultur ist gleichbedeutend mit dem Entfernen des Ornamentes aus dem Gebrauchsgegenstande.“<br><br>Adolf Loos, <i>Ornament und Verbrechen</i>, Vienna 1908.', ''),
         ('news', 'Der Standard', 'Architektur &amp; Stadt',
          'Der Standard’s pages on architecture and the city – Vienna’s buildings, housing and planning, every week.',
          'https://www.derstandard.at/immobilien/architekturundstadt'),
         # 22 Oct: Steuart's own reading list - ArchDaily, Design Museum, Architizer, DETAIL
         ('news', 'ArchDaily', 'Terra Mater Factual Studios, Hietzing',
          'The nature-film makers Terra Mater Factual Studios have extended and reorganised their offices in Vienna’s 13th district – a new building by the Austrian-Finnish office Berger Parkkinen + Architects.',
          'https://www.archdaily.com/1034207/terra-mater-factual-studios-berger-parkkinen-plus-architects'),
         ('news', 'Design Museum', 'Es Devlin: Other Worlds',
          'At the Design Museum in London until 4 April 2027: thirty years of Es Devlin’s work across sculpture, stage design, music, language and light.',
          'https://designmuseum.org/exhibitions/es-devlin-other-worlds'),
         ('news', 'Architizer', 'After the Starchitect',
          'Architizer Journal asks why 2026 feels like the end of heroic architecture – and what comes after the age of the star architect.',
          'https://architizer.com/blog/inspiration/industry/after-the-starchitect-the-end-of-heroic-architecture/'),
         ('news', 'DETAIL', 'Klimaadaptive Fassaden',
          'DETAIL 5.2026, the German building journal’s issue on climate-adaptive façades – building skins for hotter summers.',
          'https://www.detail.de/de_de/aktuelle-ausgabe-5-2026')]
CARD_AT = {2: 0, 5: 1, 9: 2, 13: 3, 17: 4, 20: 6, 22: 5, 25: 7, 28: 8, 31: 9}   # card k goes in before photo n


# ---------- wonder (23 Oct): the notebook's categories and which photo (index in BITS) sits in which - shared by phone and desktop
# six categories as title bars (23 Oct; Steuart named banality, philosophy, details - the other three are Claude's suggestions, to change)
WCATS = ['banality', 'details', 'philosophy', 'light', 'traces', 'the city', 'material', 'creatures', 'signs', 'night']   # ten since 23 Oct, 02:35 (signs, night added by Claude)   # eight since 23 Oct, 02:00; material and creatures added by Claude
WCAT_OF = {24: 0, 25: 0, 5: 0, 15: 0, 16: 0, 17: 0, 20: 2, 22: 0, 31: 0, 0: 0,
           6: 1, 12: 1, 30: 1, 32: 1, 23: 1, 1: 2, 14: 2,
           19: 3, 21: 3, 27: 3, 29: 3, 3: 3,
           2: 4, 8: 4, 18: 4, 26: 4, 28: 4, 7: 4, 9: 4, 11: 4,
           4: 5, 10: 5, 13: 5}
WCAT_OF.update({30: 6, 32: 6, 6: 6, 26: 6, 22: 7, 31: 7})   # material: shreds, torn strips, plastic, tape; creatures: the wasp, the horse
WCAT_OF.update({7: 8, 9: 8, 11: 8, 3: 9, 4: 9})   # signs: Aida, Café Prückel, the goat sign; night: the barriers and cages at night
