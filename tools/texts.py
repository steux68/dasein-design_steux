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
         '<h4>Datenschutz</h4><p>Diese Website setzt keine Cookies und erhebt keine personenbezogenen Daten. Die Karte wird von OpenStreetMap geladen. '
         '<span class="todo">[Datenschutzerklärung – bitte ergänzen]</span></p>')
