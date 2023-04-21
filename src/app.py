import json
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import random

# Load the JSON file
with open('items.json', 'r') as f:
    items_data = json.load(f)

# Create a list of items for each slot type
slot_items = {}
for item_id, item_data in items_data.items():
    slot = item_data['Slot']
    if slot not in slot_items:
        slot_items[slot] = []
    slot_items[slot].append({'label': item_data['Name'], 'value': item_id})

def slot_index(slot):
    return {'head': 0, 'face': 1, 'eyes': 2, 'pet': 3, 'body': 4}[slot]

# Define the list of benefits to display
benefit_names = [
    'HP Capacity',
    'AP Capacity',
    'Armor Power',
    'Attack Speed',
    'Luck',
    'Regen',
    'Melee Power',
    'Ranged Power',
    'Carrying Capacity',
    'Evasion',
    'Movement Speed',
    'Alchemica Speed',
    'Road Speed',
    'Vision Range',
    'HP Regen',
    'AP Regen'
]

benefit_mapping = {
    'HP Capacity': 'HP',
    'AP Capacity': 'AP',
    'Armor Power': 'defense_power',
    'Attack Speed': 'action_speed',
    'Luck': 'luck',
    'Regen': 'regen',
    'Melee Power': 'melee_power',
    'Ranged Power': 'ranged_power',
    'Carrying Capacity': 'carrying_capacity',
    'Evasion': 'evasion',
    'Movement Speed': 'movement_speed',  # Add this if there's no corresponding attribute in the Gotchi class
    'Road Speed': 'road_speed',
    'Alchemica Speed': 'alchemica_speed',
    'Vision Range': 'vision_range',
    'HP Regen': 'hp_regen',
    'AP Regen': 'ap_regen'
}

# Assuming you have an item_data dictionary
item_data = {
    "Name": "Example Item",
    "Type": "Example Type",
    "Rarity": "Common",
    "Benefits": {benefit: 0 for benefit in benefit_names}
}

def generate_item_benefits(item_id):
    if item_id is None:
        return None
    item_data = items_data[item_id]
    benefits = [html.P([html.Strong(f"{item_data['Name']}")], style={"margin-bottom": "0px"})]
    for benefit in benefit_names:
        if benefit in item_data:
            benefits.append(html.P(f"\t{benefit}: {item_data[benefit]}"))
    return benefits

class Gotchi:
    def __init__(self, NRG, AGG, SPK, BRN, BRS, base=False):
        self.NRG = NRG
        self.AGG = AGG
        self.SPK = SPK
        self.BRN = BRN
        self.BRS = BRS

        self.HP = self.calculate_hp(base)
        self.AP = self.calculate_ap(base)
        self.defense_power = self.calculate_defense_power(base)
        self.action_speed = self.calculate_action_speed(base)
        self.luck = self.calculate_luck(base)
        self.regen = self.calculate_regen(base)
        self.melee_power = self.calculate_melee_power(base)
        self.ranged_power = self.calculate_ranged_power(base)
        self.carrying_capacity = self.calculate_carrying_capacity(base)
        self.evasion = self.calculate_evasion(base)
        self.movement_speed = 21
        self.road_speed = 42
        self.alchemica_speed = 14.7
        self.vision_range = 100
        self.hp_regen = self.calculate_hp_regen(base)
        self.ap_regen = self.calculate_ap_regen(base)

    def calculate_hp(self, base=False):
        base_hp = 1000
        if base or self.NRG >= 50:
            return base_hp
        else:
            return base_hp + 10 * (50 - self.NRG)

    def calculate_ap(self, base=False):
        base_ap = 100
        if base or self.NRG < 50:
            return base_ap
        else:
            return base_ap + 1 * (self.NRG - 49)

    def calculate_defense_power(self, base=False):
        if base or self.AGG >= 50:
            return 0
        else:
            return 1 * (50 - self.AGG)

    def calculate_action_speed(self, base=False):
        base_speed = 1
        if base or self.AGG < 50:
            return base_speed
        else:
            return base_speed + 0.01 * (self.AGG - 49)

    def calculate_luck(self, base=False):
        base_luck = 1
        if base or self.SPK < 50:
            return base_luck
        else:
            return base_luck + 0.005 * (self.SPK - 49)

    def calculate_regen(self, base=False):
        base_regen = 1
        if base or self.SPK >= 50:
            return base_regen
        else:
            return base_regen + 0.01 * (50 - self.SPK)

    def calculate_melee_power(self, base=False):
        base_melee_power = 100
        if base or self.BRN < 50:
            return base_melee_power + 1.5 * (50 - self.BRN)
        else:
            return base_melee_power

    def calculate_ranged_power(self, base=False):
        base_ranged_power = 100
        if base or self.BRN >= 50:
            return base_ranged_power + 1 * (self.BRN - 49)
        else:
            return base_ranged_power

    def calculate_carrying_capacity(self, base=False):
        base_capacity = 100
        if base or self.BRS < 0:
            return base_capacity
        else:
            return base_capacity + 100 * (self.BRS/300) * (self.BRS/300)

    def calculate_evasion(self, base=False):
        if base:
            return 0
        else:
            return (self.luck - 1) ** 2

    def calculate_hp_regen(self, base=False):
        if base:
            return 2.5
        else:
            return 2.5 * self.regen

    def calculate_ap_regen(self, base=False):
        if base:
            return 7.5
        else:
            return 7.5 * self.regen

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server



app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Gotchi Stats Calculator"), className="mb-4 mt-4")
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Form([
                    dbc.Label("Enter Gotchi Traits", className="my-label"),
                    html.Div([html.Label("Enter NRG value: ", className="input-label"), dbc.Input(id="NRG-input", type="number", placeholder="NRG", min=-25, max=125, value=random.randint(-25,125), step=1, style={"width": "100px"})], title="Enter NRG value (-25 to 125)"),
                    html.Div([html.Label("Enter AGG value: ", className="input-label"), dbc.Input(id="AGG-input", type="number", placeholder="AGG", min=-25, max=125, value=random.randint(-25,125), step=1, style={"width": "100px"})], title="Enter AGG value (-25 to 125)"),
                    html.Div([html.Label("Enter SPK value: ", className="input-label"), dbc.Input(id="SPK-input", type="number", placeholder="SPK", min=-25, max=125, value=random.randint(-25,125), step=1, style={"width": "100px"})], title="Enter SPK value (-25 to 125)"),
                    html.Div([html.Label("Enter BRN value: ", className="input-label"), dbc.Input(id="BRN-input", type="number", placeholder="BRN", min=-25, max=125, value=random.randint(-25,125), step=1, style={"width": "100px"})], title="Enter BRN value (-25 to 125)"),
                    html.Div([html.Label("Enter BRS value: ", className="input-label"), dbc.Input(id="BRS-input", type="number", placeholder="BRS", min=300, max=1100, value=random.randint(300,1100), step=1, style={"width": "100px"})], title="Enter BRS value (300 to 1100)"),
                ]),
                html.Br(),
            ]),
            dbc.Col([
                dbc.Label("Equip Wearables", className="my-label"),
                html.Div(dcc.Dropdown(id='head-item-dropdown', options=slot_items['head'], placeholder="Select Head Item", style={"width": "200px"}), title="Select a Head item"),
                html.Div(dcc.Dropdown(id='face-item-dropdown', options=slot_items['face'], placeholder="Select Face Item", style={"width": "200px"}), title="Select a Face item"),
                html.Div(dcc.Dropdown(id='eyes-item-dropdown', options=slot_items['eyes'], placeholder="Select Eyes Item", style={"width": "200px"}), title="Select an Eyes item"),
                html.Div(dcc.Dropdown(id='body-item-dropdown', options=slot_items['body'], placeholder="Select Body Item", style={"width": "200px"}), title="Select a Body item"),
                html.Div(dcc.Dropdown(id='left-hand-item-dropdown', options=slot_items['hands'], placeholder="Select Left Hand Item", style={"width": "200px"}), title="Select a Left Hand item"),
                html.Div(dcc.Dropdown(id='right-hand-item-dropdown', options=slot_items['hands'] + slot_items['right hand'], placeholder="Select Right Hand Item", style={"width": "200px"}), title="Select a Right Hand item"),
                html.Div(dcc.Dropdown(id='pet-item-dropdown', options=slot_items['pet'], placeholder="Select Pet Item", style={"width": "200px"}), title="Select a Pet item"),
            ]),
            dbc.Col([
                dbc.Label("Total Gotchi Stats", className="my-label"),
                html.Div(id="stats-output")
            ]),
            dbc.Col([
                dbc.Label("Item Benefits", className="my-label"),
                html.Div(id="head-item-benefits"),
                html.Div(id="face-item-benefits"),
                html.Div(id="eyes-item-benefits"),
                html.Div(id="body-item-benefits"),
                html.Div(id="left-hand-item-benefits"),
                html.Div(id="right-hand-item-benefits"),
                html.Div(id="pet-item-benefits"),
            ])

        ])
    ])
])

@app.callback(
    Output("stats-output", "children"),
    [
        Input("NRG-input", "value"),
        Input("AGG-input", "value"),
        Input("SPK-input", "value"),
        Input("BRN-input", "value"),
        Input("BRS-input", "value"),
        Input("head-item-dropdown", "value"),
        Input("face-item-dropdown", "value"),
        Input("eyes-item-dropdown", "value"),
        Input("pet-item-dropdown", "value"),
        Input("body-item-dropdown", "value"),
        Input("left-hand-item-dropdown", "value"),
        Input("right-hand-item-dropdown", "value"),
    ]
)
def update_stats(NRG, AGG, SPK, BRN, BRS, head_item, face_item, eyes_item, pet_item, body_item, left_hand_item, right_hand_item):
    base_gotchi = Gotchi(50, 50, 50, 50, 450, base=True)
    trait_gotchi = Gotchi(NRG, AGG, SPK, BRN, BRS)

    equipped_items = [head_item, face_item, eyes_item, pet_item, body_item, left_hand_item, right_hand_item]

    item_benefits = {benefit: 0 for benefit in benefit_names}
    for item_id in equipped_items:
        if item_id is not None:
            item_data = items_data[item_id]
            for benefit in benefit_names:
                if benefit in item_data:
                    item_benefits[benefit] += item_data[benefit]

    gotchi = Gotchi(NRG, AGG, SPK, BRN, BRS)
    for benefit_name, attribute_name in benefit_mapping.items():
        if attribute_name is not None and benefit_name != 'Evasion':  # Exclude 'Evasion' from this loop
            gotchi.__dict__[attribute_name] += item_benefits[benefit_name]

    total_evasion = gotchi.calculate_evasion() + item_benefits['Evasion']
    gotchi.evasion = total_evasion

    stats_rows = []
    for benefit_name in benefit_names:
        attribute_name = benefit_mapping.get(benefit_name)
        if attribute_name is not None:
            base_value = round(base_gotchi.__dict__[attribute_name], 2)
            trait_boost = round(trait_gotchi.__dict__[attribute_name] - base_value, 2)
            total_value = round(gotchi.__dict__[attribute_name], 2)
        else:
            base_value = 0
            trait_boost = 0
            total_value = round(item_boost, 2)
        if benefit_name == 'Evasion':
            base_value = round(base_value * 100, 2)
            trait_boost = round(trait_boost * 100, 2)
            item_boost = round(item_boost * 100, 2)
            total_value = round(total_value * 100, 2)
        item_boost = round(item_benefits[benefit_name], 2)
        stats_rows.append(
            html.Tr([
                html.Td(benefit_name, style={'width': '200px'}),
                html.Td(f'{base_value}%') if benefit_name == 'Evasion' else html.Td(base_value),
                html.Td(f'{trait_boost}%') if benefit_name == 'Evasion' else html.Td(trait_boost),
                html.Td(f'{item_boost}%') if benefit_name == 'Evasion' else html.Td(item_boost),
                html.Td(f'{total_value}%') if benefit_name == 'Evasion' else html.Td(total_value)
            ])
        )

    stats_table = dbc.Table([
        html.Thead(html.Tr([html.Th("Stat"), html.Th("Base Value"), html.Th("Trait Boost"), html.Th("Item Boost"), html.Th("Total Value")])),
        html.Tbody(stats_rows)
    ])
    return stats_table

@app.callback(
    Output("head-item-benefits", "children"),
    [Input("head-item-dropdown", "value")]
)
def update_head_item_benefits(head_item_id):
    return generate_item_benefits(head_item_id)

@app.callback(
    Output("face-item-benefits", "children"),
    [Input("face-item-dropdown", "value")]
)
def update_face_item_benefits(face_item_id):
    return generate_item_benefits(face_item_id)

@app.callback(
    Output("eyes-item-benefits", "children"),
    [Input("eyes-item-dropdown", "value")]
)
def update_eyes_item_benefits(eyes_item_id):
    return generate_item_benefits(eyes_item_id)

@app.callback(
    Output("pet-item-benefits", "children"),
    [Input("pet-item-dropdown", "value")]
)
def update_pet_item_benefits(pet_item_id):
    return generate_item_benefits(pet_item_id)

@app.callback(
    Output("body-item-benefits", "children"),
    [Input("body-item-dropdown", "value")]
)
def update_body_item_benefits(body_item_id):
    return generate_item_benefits(body_item_id)

@app.callback(
    Output("left-hand-item-benefits", "children"),
    [Input("left-hand-item-dropdown", "value")]
)
def update_left_hand_item_benefits(left_hand_item_id):
    return generate_item_benefits(left_hand_item_id)

@app.callback(
    Output("right-hand-item-benefits", "children"),
    [Input("right-hand-item-dropdown", "value")]
)
def update_right_hand_item_benefits(right_hand_item_id):
    return generate_item_benefits(right_hand_item_id)

if __name__ == "__main__":
    app.run_server(debug=True)