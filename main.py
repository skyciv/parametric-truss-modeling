import skyciv
import json
import math

### Auth ###
# Find your API key here: https://platform.skyciv.com/account/api
auth = {
    "username": "YOUR_USERNAME",
    "key": "YOUR_API_KEY"
}

### Input Parameters ###
height = 5
width = 10
spaces = 2

### Calculations ###
middle_point = width / 2

start_point_coords = {
    "x": 0,
    "y": 0,
    "z": 0
}
middle_point_coords = {
    "x": middle_point,
    "y": height,
    "z": 0
}
end_point_coords = {
    "x": width,
    "y": 0,
    "z": 0
}

length_top_chord = math.sqrt(
    (middle_point_coords["x"] - start_point_coords["x"])**2 +
    (middle_point_coords["y"] - start_point_coords["y"])**2 +
    (middle_point_coords["z"] - start_point_coords["z"])**2
)

step = length_top_chord / spaces

node_index = 4

### Nodes ###

unit_vector_left_top_chord = [
    (middle_point_coords["x"] - start_point_coords["x"]) / length_top_chord,
    (middle_point_coords["y"] - start_point_coords["y"]) / length_top_chord,
    (middle_point_coords["z"] - start_point_coords["z"]) / length_top_chord
]

left_top_chord_coords = {}

for space_number in range(1, spaces):
    left_top_chord_coords[node_index] = {
        "x": start_point_coords["x"] + unit_vector_left_top_chord[0] * step * space_number,
        "y": start_point_coords["y"] + unit_vector_left_top_chord[1] * step * space_number,
        "z": start_point_coords["z"] + unit_vector_left_top_chord[2] * step * space_number
    }

    node_index += 1

unit_vector_right_top_chord = [
    (end_point_coords["x"] - middle_point_coords["x"]) / length_top_chord,
    (end_point_coords["y"] - middle_point_coords["y"]) / length_top_chord,
    (end_point_coords["z"] - middle_point_coords["z"]) / length_top_chord
]

right_top_chord_coords = {}

for space_number in range(1, spaces):
    right_top_chord_coords[node_index] = {
        "x": middle_point_coords["x"] + unit_vector_right_top_chord[0] * step * space_number,
        "y": middle_point_coords["y"] + unit_vector_right_top_chord[1] * step * space_number,
        "z": middle_point_coords["z"] + unit_vector_right_top_chord[2] * step * space_number
    }

    node_index += 1

# Bottom Chord

bottom_chord_coords = {}

middle_top_coords = {
    **left_top_chord_coords,
    '2': middle_point_coords,
    **right_top_chord_coords,
}

for coords in middle_top_coords.values():
    bottom_chord_coords[node_index] = {
        "x": coords["x"],
        "y": 0,
        "z": 0
    }

    node_index += 1

nodes = {
    '1': start_point_coords,
    '2': middle_point_coords,
    '3': end_point_coords,
    **left_top_chord_coords,  # ** is the spread operator
    **right_top_chord_coords,
    **bottom_chord_coords
}

### Supports ###

supports = {
    '1': {
        'node': 1,
        'restraint_code': 'FFFFFF'
    },
    '2': {
        'node': 3,
        'restraint_code': 'RFFRRR'
    },
}

### Sections ###

sections = {
    "1": {
        "load_section": ["American", "AISC", "W shapes", "W4x13"],
        "material_id": 1
    }
}

### Members ###

members = {
    "1": {
        "node_A": 1,
        "node_B": 4,
        "fixity_A": "FFFFRR",
        "fixity_B": "FFFFRR",
        "section_id": 1
    },
    "2": {
        "node_A": spaces + 2,
        "node_B": 2,
        "fixity_A": "FFFFRR",
        "fixity_B": "FFFFRR",
        "section_id": 1
    },
    "3": {
        "node_A": 2,
        "node_B": spaces + 3,
        "fixity_A": "FFFFRR",
        "fixity_B": "FFFFRR",
        "section_id": 1
    },
    "4": {
        "node_A": spaces * 2 + 1,
        "node_B": 3,
        "fixity_A": "FFFFRR",
        "fixity_B": "FFFFRR",
        "section_id": 1
    },
    "5": {
        "node_A": 1,
        "node_B": spaces * 2 + 2,
        "fixity_A": "FFFFRR",
        "fixity_B": "FFFFRR",
        "section_id": 1
    },
    "6": {
        "node_A": spaces * 4,
        "node_B": 3,
        "fixity_A": "FFFFRR",
        "fixity_B": "FFFFRR",
        "section_id": 1
    },
    "7": {
        "node_A": 2,
        "node_B": spaces * 3 + 1,
        "fixity_A": "FFFFRR",
        "fixity_B": "FFFFRR",
        "section_id": 1
    },
}

member_index = 8  # Start at 8 because we already have 7 members

# Left side
start_node_left_side = 4
end_node_left_side = spaces + 2

for node in range(start_node_left_side, end_node_left_side + 1):

    # Vertical members
    members[member_index] = {
        'node_A': node,
        'node_B': node + spaces * 2 - 2,
        'fixity_A': 'FFFFRR',
        'fixity_B': 'FFFFRR',
        'section_id': 1
    }

    member_index += 1

    # Diagonal members
    members[member_index] = {
        'node_A': node,
        'node_B': node + spaces * 2 - 1,
        'fixity_A': 'FFFFRR',
        'fixity_B': 'FFFFRR',
        'section_id': 1
    }

    member_index += 1

    # Top chord
    if (node != end_node_left_side):

        members[member_index] = {
            'node_A': node,
            'node_B': node + 1,
            'fixity_A': 'FFFFRR',
            'fixity_B': 'FFFFRR',
            'section_id': 1
        }

        member_index += 1

    # Bottom chord
    members[member_index] = {
        'node_A': node + spaces * 2 - 2,
        'node_B': node + spaces * 2 - 1,
        'fixity_A': 'FFFFRR',
        'fixity_B': 'FFFFRR',
        'section_id': 1
    }

    member_index += 1

# rigth side
start_node_right_side = spaces + 3
end_node_right_side = spaces * 2 + 1

for node in range(start_node_right_side, end_node_right_side + 1):

    # Vertical member
    members[member_index] = {
        "node_A": node,
        "node_B": node + spaces * 2 - 1,
        "fixity_A": "FFFFRR",
        "fixity_B": "FFFFRR",
        "section_id": 1
    }

    member_index += 1

    # Diagonal member
    members[member_index] = {
        "node_A": node,
        "node_B": node + spaces * 2 - 2,
        "fixity_A": "FFFFRR",
        "fixity_B": "FFFFRR",
        "section_id": 1
    }

    member_index += 1

    # Top chord
    if (node != end_node_right_side):

        members[member_index] = {
            "node_A": node,
            "node_B": node + 1,
            "fixity_A": "FFFFRR",
            "fixity_B": "FFFFRR",
            "section_id": 1
        }

        member_index += 1

    # Bottom chord
    members[member_index] = {
        "node_A": node + spaces * 2 - 2,
        "node_B": node + spaces * 2 - 1,
        "fixity_A": "FFFFRR",
        "fixity_B": "FFFFRR",
        "section_id": 1
    }

    member_index += 1

### Point loads ###

point_loads = {
    "1": {
        "type": "n",
        "node": 2,
        "x_mag": 0,
        "y_mag": -10,
        "z_mag": 0,
        "load_group": "DL"
    },
    "2": {
        "type": "n",
        "node": 4,
        "x_mag": 0,
        "y_mag": -5,
        "z_mag": 0,
        "load_group": "DL"
    },
    "3": {
        "type": "n",
        "node": spaces * 2 + 1,
        "x_mag": 0,
        "y_mag": -5,
        "z_mag": 0,
        "load_group": "DL"
    }
}

model = {
    'nodes': nodes,
    'supports': supports,
    'sections': sections,
    'members': members,
    'point_loads': point_loads,
}

request_data = {
    "auth": auth,
    "functions": [
        {
            "function": "S3D.session.start",
        },
        {
            "function": "S3D.model.set",
            "arguments": {
                "s3d_model": model
            }
        },
        {
            "function": "S3D.model.solve",
            "arguments": {
                "analysis_type": "linear",
                "repair_model": True,
                "result_filter": ["member_forces", "member_displacements"]
            }
        },
        {
            "function": "S3D.file.save",
            "arguments": {
                "name": "Parametric Truss V2",
                "path": "api/",
                "public_share": False
            }
        },
    ]
}

request = skyciv.request(request_data)

print(json.dumps(request, indent=4))
