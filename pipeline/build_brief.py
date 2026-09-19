import json, os, re, shutil
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from pypdf import PdfReader

TITLE='Coffee & Snack Shops in the US'
def cite(page,section): return f'IBISWorld, {TITLE}, June 2026, printed p. {page}, {section}.'
sections=[]
def add(title, paragraphs, table=None): sections.append(dict(title=title,paragraphs=paragraphs,table=table))
add('Company and industry',[
 'Company: Starbucks. The selected scope is U.S. coffee and snack shop operations, within the specialty coffee retail industry. The report identifies Starbucks as a specialty coffee company with a global store network; its industry definition covers prepared specialty snacks and nonalcoholic beverages consumed on-site, taken away or delivered. '+cite('1 and 32','About This Industry / Definition; Company Details / Starbucks'),
 'Coverage mismatch: the U.S. industry includes ice cream, bagel, donut and other snack shops in addition to coffee shops. It is broader than a coffee-only market, but narrower geographically and operationally than Starbucks as a consolidated global company. Manufacturing, coffee production and tea production are separately identified activities. The brief therefore does not treat this industry as Starbucks\' entire addressable global market. Interpretation based on '+cite('1 and 32','Definition; Company Details / Other Industries')])
add('NAICS code and reason for choosing it',[
 'Proposed six-digit code: 722515 - Snack and Nonalcoholic Beverage Bars (2022 NAICS), for the selected U.S. coffee-shop activity. IBISWorld maps this report to that code. '+cite('1','Codes'),
 'Official comparison: 722515 covers specialty snacks and nonalcoholic beverages and explicitly includes on-premise brewing coffee shops; neighboring 722513, Limited-Service Restaurants, covers food service with ordering/payment before eating while excluding snack and nonalcoholic beverage bars. Source: U.S. Census Bureau / OMB, 2022 NAICS United States Manual, printed pp. 562-563, entries 722513 and 722515 (PDF pages 564-565).',
 'Choice in one sentence: 722515 is the better fit because Starbucks\' selected coffee-store activity centers on specialty nonalcoholic beverages, whereas 722513 covers limited-service meals and explicitly excludes beverage bars. Interpretation based on '+cite('32','Company Details / Description')+' Census / OMB, 2022 NAICS Manual, printed pp. 562-563, entries 722513 and 722515.',
 'Classification limit: this is a proposed activity-level classification, not verification of a corporate filing or the code for every Starbucks establishment; confirm the specific entity and revenue mix if analyzing roasting, packaged products or another business segment.'])
add('Industry size, year, geography and five-year growth trajectory',[
 'The U.S. industry is estimated at $75,451.1 million ($75.45 billion) in 2026. The report was published mid-year, so its 2026 value is an estimate, not a completed-year historical actual. It forecasts $77,815.6 million in 2031. '+cite('45','Key Statistics / Industry Data, Values table, Revenue ($m) column; 2026 and 2031 rows'),
 'Reported five-year growth: 2.5% annualized for 2021-2026 (historical period ending in the current-year estimate) and 0.6% annualized for the 2026-2031 forecast. '+cite('4','At a Glance / Revenue; historic and forecast CAGR note'),
 'Calculated historical-to-estimate CAGR: [(75,451.1 / 66,718.4)^(1/5) - 1] x 100 = 2.49% for 2021-2026. Calculated forecast CAGR: [(77,815.6 / 75,451.1)^(1/5) - 1] x 100 = 0.619% for 2026-2031. Both calculations use the same U.S. industry revenue series in millions of dollars. '+cite('45','Industry Data, Values table'),
 'Interpretation: the forecast implies slower revenue expansion than the preceding five-year period; it should not be read as a forecast for Starbucks\' own revenue. '+cite('4 and 45','Revenue CAGR summary; Industry Data')],
 {'headers':['Year','Revenue ($ millions)','Status'], 'rows':[['2021','66,718.4','Historical'],['2025','75,598.5','Historical / report estimate'],['2026','75,451.1','Current-year estimate'],['2027','75,619.3','Forecast'],['2028','75,971.0','Forecast'],['2029','76,434.5','Forecast'],['2030','77,104.2','Forecast'],['2031','77,815.6','Forecast']], 'citation':cite('45','Industry Data, Values table')})
add('Competitors and industry market shares',[
 'Benchmark: Starbucks is the report\'s only separately quantified major player, with a reported 30.1% industry share and $22.7 billion of industry-specific revenue in 2026. All other companies together account for 69.9%. These are U.S. coffee-and-snack industry measures, not worldwide coffee shares. '+cite('30 and 32','Industry Market Share by Company chart; Company Details / 2026 metrics'),
 'Five report-listed rivals are shown below. Their reported 0-2.5% bands do not identify an exact share or rank them as the largest five competitors. The company table itself has no separate year label; its placement in the 2026 report is context, not independent confirmation of the date of each band. '+cite('30-31','Companies / Company Market Share (%) table'),
 'Dunkin\' Donuts is also named in the narrative, but no standalone share for it was found in the supplied Companies table. Do not convert a narrative mention into a numerical share or substitute a global brand sales figure. '+cite('5 and 30-31','Executive Summary; Companies tables'),
 'Not found: a defensible ranking of the top three to five rivals with precise, same-year shares. Obtain the full IBISWorld interactive company data or audited U.S. in-scope sales with a matching industry denominator. The report warns that its PDF chart is simplified. '+cite('30','Market Share chart note')],
 {'headers':['Report-listed competitor','Reported share','Location in report'], 'rows':[['Dutch Bros','0-2.5% (range)','Printed p. 30'],['Baskin-Robbins','0-2.5% (range)','Printed p. 30'],["Bruster\'s",'0-2.5% (range)','Printed p. 31'],['Better Buzz Coffee','0-2.5% (range)','Printed p. 31'],['Blue Bottle Coffee','0-2.5% (range)','Printed p. 31']], 'citation':cite('30-31','Companies / Company Market Share (%) tables')})
add('Regulatory or compliance pressure',[
 'The report assesses regulation as moderate and increasing. It describes food safety rules shaped by the FDA Model Food Code, which it correctly distinguishes from the enforceable rules adopted by state and local authorities. It also identifies federal, state and local wage compliance as a recurring operating cost pressure. These are report-described pressures as of June 2026, not a current jurisdiction-specific compliance determination. '+cite('35','Regulation & Policy / FDA; Fair Labor Standards Act minimum wage'),
 'Starbucks-specific labor exposure: the report describes an expanding union presence and potential changes to scheduling, grievance handling and negotiated terms. Interpretation: compliance and bargaining complexity may limit near-term staffing flexibility, although lower turnover could offset some costs. '+cite('32','Company Details / Expanding union presence'),
 'Franchising regulation is discussed at industry level; its applicability to a particular Starbucks operating or licensing arrangement requires separate review. Not found: a store-by-store legal requirements inventory. Obtain the relevant local rules and company labor/licensing disclosures. '+cite('35','Regulation & Policy / Franchising laws')])
add('Supply chain concentration or fragility',[
 'Fragility is supported more clearly than numerical supplier concentration: the report describes weather-sensitive coffee harvests, difficulty passing input costs through to menu prices, tariff-driven sourcing shifts and freight disruption. It rates supplier power high and increasing. '+cite('29','Buyer & Supplier Power / Supplier: cost volatility'),
 'The supply-chain diagram links operators to coffee producers; confectionery, dairy and produce wholesalers; grocery wholesalers; and equipment suppliers. The diagram maps industry relationships rather than vendor-level spending shares. '+cite('28','Buyer & Supplier Power / Supply Chain diagram'),
 'Interpretation: specialized bean quality, input volatility and costly equipment substitution create exposure even where multiple vendors exist. No supplier concentration ratio, country-level procurement shares or Starbucks-specific hedge coverage is established by the report. Obtain supplier spend, origin mix, contract terms and inventory/hedging disclosures before quantifying the exposure. '+cite('28-29','Supply Chain diagram; Supplier power discussion')])
add('Customer concentration or fragmentation',[
 'The industry serves a broad consumer base: IBISWorld labels customer-class concentration low, and its supply-chain diagram identifies consumers as the first-tier buyer industry. This supports a fragmented customer-base interpretation, not a measured Starbucks customer concentration ratio. '+cite('5 and 28','SWOT / Strengths; Supply Chain diagram'),
 'The 2026 Major Markets Segmentation chart attributes 23.7% of revenue to households earning $100,000-$149,999, 23.6% to households above $150,000, and 6.4% to businesses. Calculated: the two highest-income groups sum to 47.3% (23.7 + 23.6). This describes income-segment exposure, not dependence on a few individual customers. '+cite('19','Major Markets Segmentation chart'),
 'Source inconsistency: the preceding narrative gives 32.9% for the $30,000-$70,000 group in 2025, while the 2026 chart assigns 22.5% to $30,000-$69,999 and separately 10.5% to $70,000-$99,999. The year and category mismatch should be checked; do not merge those statements into one comparable series. '+cite('18-19','Major Markets narrative and Segmentation chart'),
 'Not found: Starbucks\' top-customer revenue share, repeat-customer concentration or loyalty-cohort dependence. Request transaction-level concentration analysis and company customer metrics.'])
add('Biggest trend over the next five years',[
 'Interpretation for 2026-2031: technology-enabled service efficiency is the most consequential operating trend in this brief. IBISWorld\'s outlook discusses automated preparation, mobile ordering, self-service kiosks, equipment monitoring and digital payments as ways to improve consistency and reduce workload. The source does not rank one trend as definitively biggest. '+cite('11','Outlook / Innovative AI technology elevates industry standards'),
 'Supporting quote (six words): "Innovative AI technology elevates industry standards". '+cite('11','Outlook subsection heading'),
 'Implication for Starbucks: use digital convenience and selective automation without eroding the in-store experience. This is an interpretation, supported by the report\'s separate account of Starbucks moving away from pickup-only formats and improving traditional cafes. The report supplies no quantified five-year return on those investments. '+cite('11 and 33','Technology outlook; Starbucks pivots away from Pickup-Only stores')])
add('Biggest threat over the next five years',[
 'Interpretation for 2026-2031: persistent margin compression from volatile coffee, freight and labor costs is the most important threat in this brief, because suppliers\' leverage can coincide with price-sensitive buyers and strong competition. The report supports those mechanisms but does not supply probabilities or a ranked risk model. '+cite('28-29 and 37-38','Buyer & Supplier Power; Cost Structure / wage and coffee costs'),
 'The industry\'s 2026 profit margin is estimated at 5.6%, with wages taking 31.7% of revenue. These industry benchmarks are not Starbucks\' own margins. Interpretation: they indicate limited room for industry operators to absorb cost shocks while protecting customer value. '+cite('37','Financial Benchmarks / Profit Margin and Cost Structure Benchmarks'),
 'Verification limit: tariff and conflict-related statements in the report are time-sensitive. Confirm current policy, sourcing exposure and freight conditions before using them for a decision; no specific future tariff rate is assumed here. '+cite('29','Supplier power discussion')])
add('Missing information and sources needed',[
 'Not found - precise rival rankings and shares: the report provides one exact major-player share and broad ranges for other companies. Needed: full interactive IBISWorld company data and same-year, same-geography, same-industry sales. '+cite('30-31','Companies / Market Share and tables'),
 'Not found - Starbucks\' complete global market coverage: this report covers one U.S. industry. Needed: Starbucks annual report/segment disclosures and country-specific industry reports, with retail and manufacturing activities separated. '+cite('1 and 32','Definition; Company Details'),
 'Not found - supplier spend concentration and risk mitigation: needed procurement-by-supplier and origin data, hedge disclosures, contract lengths and contingency plans. The supplied evidence is qualitative. '+cite('28-29','Buyer & Supplier Power'),
 'Not found - customer-level concentration: needed transaction or account-level revenue distribution; income bands are not individual customer concentration. '+cite('18-19','Major Markets'),
 'Not found - quantified five-year trend and threat impacts: needed scenario models, unit economics, investment plans and evidence-based assumptions for adoption, pricing and input costs. '+cite('10-12 and 37-38','Outlook; Cost Structure'),
 'Unresolved - customer-segment comparability and competitor table dates: obtain the publisher\'s underlying tables or an explanation of the category/year labels. Needed for a consistent comparative dataset. '+cite('18-19 and 30-31','Major Markets; Companies tables')])

brief={'company':'Starbucks','scope':'U.S. coffee & snack shop operations','coverage':[
 'Primary report: IBISWorld, Coffee & Snack Shops in the US, industry 72221B, Valerie Le, published June 2026 (cover, PDF page 1). Geography: United States; activity definition: printed p. 1. Main forecast: 2026-2031 (printed p. 10, Outlook). The Industry Data table extends through 2032 (printed p. 45); this brief uses the requested five-year window.',
 'Classification reference: U.S. Census Bureau / OMB, 2022 NAICS United States Manual, printed pp. 562-563, entries 722513 and 722515. https://www.census.gov/naics/reference_files_tools/2022_NAICS_Manual.pdf',
 'Coverage boundary: U.S. retail coffee and snack operations only. The report does not cover all Starbucks countries or activities. All IBISWorld citations below use printed page numbers; printed p. 1 is PDF page 4.'], 'sections':sections,'verification':[
 'Confirm the 2026 estimate and 2031 forecast in the Industry Data table, printed p. 45; do not label 2026 as a completed-year actual.',
 'Confirm the competitor ranges and their underlying observation dates, printed pp. 30-31; request exact values before ranking rivals.',
 'Resolve the income-group and year mismatch between printed pp. 18-19; verify chart totals and definitions.',
 'Confirm 722515 for the selected operating activity; use a separate classification for a different company segment.',
 'Check current local labor/food rules and tariff/freight conditions against authoritative sources before acting on the report\'s June 2026 narrative.',
 'Review the analyst-selected trend and threat priorities against the original evidence; they are interpretations, not publisher rankings.']}
os.makedirs('dist',exist_ok=True)
os.makedirs('outputs',exist_ok=True)
open('dist/starbucks-brief.json','w',encoding='utf-8').write(json.dumps(brief,ensure_ascii=False,indent=2))
style=getSampleStyleSheet()
style.add(ParagraphStyle(name='TitleX',fontName='Helvetica-Bold',fontSize=30,leading=35,textColor=colors.HexColor('#173f32'),spaceAfter=13))
style.add(ParagraphStyle(name='SubX',fontSize=12,leading=18,textColor=colors.HexColor('#56675e'),spaceAfter=20))
style.add(ParagraphStyle(name='HeadX',fontName='Helvetica-Bold',fontSize=14,leading=19,spaceBefore=16,spaceAfter=11,textColor=colors.HexColor('#175c48'),keepWithNext=True))
style.add(ParagraphStyle(name='BodyX',fontName='Helvetica',fontSize=10,leading=15,spaceAfter=11))
style.add(ParagraphStyle(name='SmallX',fontSize=8,leading=11,spaceAfter=9,textColor=colors.HexColor('#5d6c65')))
style.add(ParagraphStyle(name='CellX',fontSize=9,leading=13))
story=[]
def p(t,s='BodyX'):return Paragraph(escape(t),style[s])
story+=[p('FIELDNOTE / INDUSTRY INTELLIGENCE','SmallX'),Spacer(1,13),p('Starbucks','TitleX'),p('U.S. Coffee & Snack Shops\nIndustry intelligence brief','SubX'),p('Report coverage and analytical boundaries','HeadX')]
story += [p(t) for t in brief['coverage']]
for i,s in enumerate(sections):
 if i in [1,2,3,4,6,8,9]:story.append(PageBreak())
 story.append(p(f'{i+1:02d}  {s["title"]}','HeadX'))
 for t in s['paragraphs']:story.append(p(t))
 if s['table']:
  tb=s['table'];data=[[p(v,'CellX') for v in row] for row in [tb['headers']]+tb['rows']]
  table=Table(data,colWidths=[157,157,157],repeatRows=1,hAlign='LEFT');table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e9f1ec')),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,-1),.4,colors.HexColor('#d9e2dc'))]));story.extend([table,Spacer(1,9),p(tb['citation'],'SmallX')])
story.append(p('Verification needed','HeadX'));story.extend(p('- '+t) for t in brief['verification'])
def footer(c,d):
 c.setStrokeColor(colors.HexColor('#dce5df'));c.line(48,41,564,41);c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#617569'));c.drawString(48,27,'FIELDNOTE  /  STARBUCKS  /  Source edition: June 2026');c.drawRightString(564,27,str(d.page))
path='outputs/Starbucks-Industry-Intelligence-Brief.pdf'
SimpleDocTemplate(path,pagesize=(612,792),rightMargin=48,leftMargin=48,topMargin=43,bottomMargin=58,title='Starbucks | Industry Intelligence Brief',author='Fieldnote').build(story,onFirstPage=footer,onLaterPages=footer)
shutil.copy(path,'dist/starbucks-brief.pdf')
print('Brief pages:',len(PdfReader(path).pages))
print('CAGR:',((75451.1/66718.4)**.2-1)*100,((77815.6/75451.1)**.2-1)*100)
