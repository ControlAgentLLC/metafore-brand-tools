"""Example: build a Metafore-styled white paper from the ADNOC content.

Run with:
    python3 example.py

Reads `build_doc.py` from the same directory. Outputs to the same directory
as `metafore-doc-example.docx` (change OUTPUT below).
"""

import os
import sys

# Make the library importable from this script's location
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_doc import (
    create_doc, save_doc, page_break,
    add_cover_eyebrow, add_cover_h1, add_cover_subtitle, add_cover_lead,
    add_toc_page,
    add_section_eyebrow, add_h2, add_subhead,
    add_body, add_takeaway, add_bullet,
    add_callout, add_data_table, add_signature_block,
    # Visuals — every two facing pages carry one
    add_icon, add_icon_row, add_figure, add_kpi_band, add_pull_quote,
)

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'metafore-doc-example.docx')


# ---- Configure the doc -----------------------------------------------

doc = create_doc(
    include_cover=True,
    include_toc=True,
    doc_type_label='White Paper',
    publish_date='May 2026',
    title_short='An agentic Bayesian engine for ADNOC',
    meta_labels=['Prepared for', 'Version', 'Reading time'],
    meta_values=['ADNOC', 'v1.0', '8 minutes'],
)


# ---- Cover page ------------------------------------------------------

add_cover_eyebrow(doc, 'Probabilistic Influence Network · UAE gas sector')
add_cover_h1(doc,
    'An agentic Bayesian engine for CNG and gas market ',
    'intelligence.')
add_cover_subtitle(doc,
    'A 21-node influence network sitting over a deterministic knowledge graph, for ADNOC.')
add_cover_lead(doc,
    "As the UAE accelerates its energy transition and industrial expansion, capital "
    "allocation in the natural gas and CNG sectors requires moving beyond historical "
    "reporting. ADNOC's strategic posture demands a system that answers what is about "
    "to happen, why, and which lever moves it.")
page_break(doc)


# ---- TOC page --------------------------------------------------------

add_toc_page(doc, title='Contents', max_level=2)
page_break(doc)


# ---- Body ------------------------------------------------------------

# Section 01 — first section uses no top rule (nothing above it)
add_section_eyebrow(doc, '01 · Summary', with_top_rule=False)
add_h2(doc, 'Beyond historical reporting, into probabilistic intent.')
add_callout(doc,
    "The Metafore EGI platform unifies a deterministic data layer with a probabilistic "
    "predictive engine. A 21-node Bayesian Influence Network sits over the Neo4j "
    "knowledge graph, turning fragmented market signals into actionable probability "
    "distributions across demand, infrastructure, and expansion viability.")
add_body(doc, [
    ('Traditional business intelligence tools answer ', False),
    ('what happened', True),
    ('. The platform you are proposing answers ', False),
    ('what is about to happen, why, and which lever moves it', True),
    ('. This document sets out the topology, the four causal layers that structure it, '
     'and the full 21-node framework.', False),
])
add_body(doc,
    "Anchoring the probabilistic network on a deterministic layer lets the engine handle "
    "unpredictable variables — market sentiment, geopolitical risk, mega-project timing — "
    "while the knowledge graph manages the unchanging physical reality of pipelines, "
    "fleets, and reserve capacity.")


# Section 02
add_section_eyebrow(doc, '02 · Network topology')
add_h2(doc, 'Four causal layers, twenty-one nodes.')
add_body(doc,
    'We divide the network into four causal layers, flowing from macro-level drivers '
    'down to specific business outputs. Each layer narrows uncertainty into a more '
    'concrete decision surface for the layer below.')
add_icon_row(doc, [
    ('Fan', 'Macro drivers', 'GDP, policy, and global gas pricing.'),
    ('Process', 'Sector activity', 'Power, industry, transport, real estate.'),
    ('Stack', 'Infrastructure', 'Production, pipelines, and capacity.'),
    ('Transform', 'Strategic action', 'Where and when to expand.'),
])

add_subhead(doc, '1', 'Macro-economic and policy drivers')
add_body(doc, 'Independent variables that initiate the probability chain.')
add_bullet(doc, [('UAE Economic Growth (GDP)', True),
                 (' — impacts overall energy consumption.', False)])
add_bullet(doc, [('Government Policy & Subsidies', True),
                 (' — models the aggressiveness of decarbonization mandates and fuel subsidies.', False)])
add_bullet(doc, [('Global Gas Pricing (LNG vs diesel)', True),
                 (' — the price spread dictates the economic incentive for fuel switching.', False)])

add_subhead(doc, '2', 'Sector-specific activity')
add_body(doc, 'Nodes conditionally dependent on Layer 1, mapped directly to Phase 1 requirements.')
add_bullet(doc, [('Power Generation Mix', True),
                 (' — accounts for gas-fired generation and the integration of solar and nuclear baseloads.', False)])
add_bullet(doc, [('Industrial Expansion', True),
                 (" — captures heavy manufacturing and chemical production (ADNOC's $55B investment pipeline and the TA'ZIZ hub).", False)])
add_bullet(doc, [('Transport Fleet Conversion', True),
                 (' — models CNG adoption rate in commercial logistics and public transit.', False)])
add_bullet(doc, [('Residential & Commercial Real Estate', True),
                 (' — demand driven by urbanization and cooling needs.', False)])


# Section 03 — data table example
add_section_eyebrow(doc, '03 · Complete 21-node topology')
add_h2(doc, 'The full causal framework.')
add_body(doc,
    "The table below defines the entire causal framework, moving from macro-economic "
    "independent variables down to the final strategic Expansion Action.")
add_callout(doc,
    "Mega-project timelines are the absolute high-value lever for industrial demand. "
    "An on-time TA'ZIZ project yields a 64% probability of a demand surge in Abu Dhabi; "
    "if delayed, that probability collapses below 15% in the current run of the network.")

headers = ['Node', 'Layer', 'Name', 'Discrete states', 'Parents']
col_widths = [0.55, 1.45, 1.45, 1.85, 1.7]  # sums to 7.0" — Layer column fits INFRASTRUCTURE at 9pt
rows_data = [
    [('N1','id'),('Root Driver','layer'),('Global LNG Price','name'),
     ('High, Avg, Low','states'),('— (independent)','parents')],
    [('N2','id'),('Root Driver','layer'),('UAE GDP Growth','name'),
     ('Expand, Stagnate','states'),('— (independent)','parents')],
    [('N3','id'),('Root Driver','layer'),('Gov Subsidy','name'),
     ('Favourable, Neutral, Phase-out','states'),('— (independent)','parents')],
    [('N5','id'),('Infrastructure','layer'),('Domestic Gas Production','name'),
     ('High, Stable, Deficit','states'),('N2','parents')],
    [('N12','id'),('Sector Driver','layer'),('Mega Projects','name'),
     ('On-time, Delayed','states'),('N2','parents')],
    [('N19','id'),('Regional Insight','layer'),('Abu Dhabi Total','name'),
     ('Critical, Stable','states'),('N15, N17','parents')],
    [('N21','id'),('Strategic Action','layer'),('Expansion Action','name'),
     ('Prime, Monitor, Unviable','states'),('N6, N19, N20','parents')],
]
add_data_table(doc, headers, rows_data, col_widths)

add_kpi_band(doc, [
    ('64%', "Demand-surge probability with TA'ZIZ on time"),
    ('<15%', 'The same probability if TA\'ZIZ is delayed'),
    ('21', 'Nodes in the influence network'),
    ('4', 'Causal layers'),
], source='Source: current run of the 21-node network')

add_takeaway(doc,
    "Variable Elimination collapses this 21-node graph into clean conditional probability "
    "matrices in milliseconds — the executive answer surface that drives Pulse and the "
    "conversational engine, recomputed every time new telemetry hits the root nodes.")


# (Proposals also include a signature block at the end — uncomment to use:)
# add_signature_block(doc,
#     left_label='For ADNOC', left_who='Name · Title',
#     right_label='For Metafore', right_who='Ori Sasson · CEO')


save_doc(doc, OUTPUT)
print(f'Wrote: {OUTPUT}')
