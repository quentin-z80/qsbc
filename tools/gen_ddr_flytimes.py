import pcbnew
import regex
import pprint

from openpyxl import Workbook, load_workbook

groups = [
    {"name": "Clocks", "regex": "^.*DRAM_CK_[N|P]$", "nets": []},
    {"name": "Address, Command and Control", "regex": "^.*DRAM_((A0*[0-9]+)|(BA[0-1])|(RAS)|(CAS)|(WE_B))$", "nets": []},
    {"name": "Byte Group 1", "regex": "^.*DRAM_((D0[0-7])|(DQM0)|(SDQS0_(P|N)))$", "nets": []},
    {"name": "Byte Group 2", "regex": "^.*DRAM_((D0[8-9])|(D1[0-5])|(DQM1)|(SDQS1_(P|N)))$", "nets": []},
    {"name": "Control", "regex": "^.*DRAM_((CS0)|(CKE)|(ODT))$", "nets": []},
]

#0 = name
#1 = ps / cm
layers = {
    "F.Cu": 58.5680,
    "In2.Cu": 70.7803,
    "B.Cu": 58.5680
}

package_delays = {

    "/DDR/DRAM_A00": 56.5,
    "/DDR/DRAM_A01": 42.2,
    "/DDR/DRAM_A02": 41.8,
    "/DDR/DRAM_A03": 22.4,
    "/DDR/DRAM_A04": 43.1,
    "/DDR/DRAM_A05": 32.0,
    "/DDR/DRAM_A06": 33.8,
    "/DDR/DRAM_A07": 54.8,
    "/DDR/DRAM_A08": 59.7,
    "/DDR/DRAM_A09": 35.8,
    "/DDR/DRAM_A10": 59.5,
    "/DDR/DRAM_A11": 29.1,
    "/DDR/DRAM_A12": 39.6,
    "/DDR/DRAM_A13": 31.9,
    "/DDR/DRAM_A14": 43.1,
    "/DDR/DRAM_A15": 38.6,
    "/DDR/DRAM_A16": 51.2,

    "/DDR/DRAM_D00": 47.2,
    "/DDR/DRAM_D01": 43.0,
    "/DDR/DRAM_D02": 54.6,
    "/DDR/DRAM_D03": 51.7,
    "/DDR/DRAM_D04": 59.9,
    "/DDR/DRAM_D05": 58.1,
    "/DDR/DRAM_D06": 64.6,
    "/DDR/DRAM_D07": 51.4,
    "/DDR/DRAM_D08": 45.0,
    "/DDR/DRAM_D09": 50.1,
    "/DDR/DRAM_D10": 46.2,
    "/DDR/DRAM_D11": 47.2,
    "/DDR/DRAM_D12": 40.3,
    "/DDR/DRAM_D13": 48.8,
    "/DDR/DRAM_D14": 58.4,
    "/DDR/DRAM_D15": 52.4,

    "/DDR/DRAM_DQS0_N": 58.9,
    "/DDR/DRAM_DQS0_P": 59.0,
    "/DDR/DRAM_DQS1_N": 47.2,
    "/DDR/DRAM_DQS1_P": 48.6,

    "/DDR/DRAM_DMI0": 57.2,
    "/DDR/DRAM_DMI1": 58.6,
    "/DDR/DRAM_CKE": 51.2,
    "/DDR/DRAM_CK_P": 39.1,
    "/DDR/DRAM_CK_N": 39.4,
    "/DDR/DRAM_BG0": 41.1,
    "/DDR/DRAM_BG1": 41.2,
    "/DDR/~\{DRAM_CS0\}": 35.9,
    "/DDR/~\{DRAM_ACT\}": 45.7,
    "/DDR/DRAM_BA0": 34.4,
    "/DDR/DRAM_BA1": 53.4,
    "/DDR/DRAM_ODT": 26.5,
    "/DDR/DRAM_PARITY": 29.0,
    "/DDR/~\{DRAM_RESET\}": 38.1,
    "/DDR/~\{DRAM_ALERT\}": 36.0
}

class TrackNoGroupException(Exception):
    pass

def mm_to_ps(layer: str, mm: float) -> float:
    return mm * (layers[layer] / 10)

try:
    wb = load_workbook("DDR_flytimes.xlsx")
except FileNotFoundError:
    print("DDR_flytimes.xlsx not found")
    wb = Workbook()
    wb.save("DDR_flytimes.xlsx")

def get_track_group(track) -> str:
    """
    Returns the group name of a track
    raises exception if track not in any group
    """
    #print(track.GetNetname())
    for group in groups:
        if regex.match(group["regex"], track.GetNetname()):
            return group["name"]
    raise TrackNoGroupException("Track not in any group")

def add_segment(group_name, netname, flytime):
    for group in groups:
        if group["name"] == group_name:
            for net in group["nets"]:
                if net["name"] == netname:
                    net["track_flytime"] += flytime
                    return
            group["nets"].append({"name": netname, "track_flytime": flytime})

def get_flytimes(pcb):

    pcb.BuildListOfNets()
    tracks = pcb.GetTracks()

    for track in tracks:
        if track.GetNet() is None:
            continue
        try:
            group_name = get_track_group(track)
        except TrackNoGroupException:
            continue

        if type(track) == pcbnew.PCB_VIA:
            #TODO: handle vias
            continue
        else:
            length = pcbnew.ToMM(track.GetLength())
            netname = track.GetNetname()
            layer = track.GetLayerName()
            flytime = mm_to_ps(layer, length)
            #print(f"{layer} {netname} {length}mm {flytime}ps ")
            add_segment(group_name, netname, flytime)

def write_flytimes(wb):
    ws = wb.active
    ws.title = "DDR"
    ws.cell(row=1, column=1).value = "Group"
    ws.cell(row=1, column=2).value = "Net"
    ws.cell(row=1, column=3).value = "Vias"
    ws.cell(row=1, column=4).value = "Track Flytime"
    ws.cell(row=1, column=5).value = "Via Delay"
    ws.cell(row=1, column=6).value = "Package Delay"
    ws.cell(row=1, column=7).value = "Extra Delay"
    ws.cell(row=1, column=8).value = "Total Delay"
    row = 2
    for group in groups:
        for net in group["nets"]:
            ws.cell(row=row, column=1).value = group["name"]
            ws.cell(row=row, column=2).value = net["name"].removeprefix("/DDR/")
            ws.cell(row=row, column=4).value = round(net["track_flytime"], 1)
            #TODO: calculate via delay
            ws.cell(row=row, column=5).value = 0
            if net["name"] in package_delays:
                ws.cell(row=row, column=6).value = round(package_delays[net["name"]], 1)
            else:
                ws.cell(row=row, column=6).value = 0

            ws.cell(row=row, column=8).value = round(net["track_flytime"] + 0 + package_delays[net["name"]] + ws.cell(row=row, column=7).value, 1)
            row += 1

if __name__ == "__main__":
    pcb = pcbnew.LoadBoard("../qsbc.kicad_pcb")
    get_flytimes(pcb)
    pprint.pprint(groups)
    write_flytimes(wb)
    wb.save("DDR_flytimes.xlsx")
