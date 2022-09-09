import sys

import pcbnew

from openpyxl import Workbook, load_workbook

class FlyTools:

    def __init__(self, board: pcbnew.BOARD):
        self.board = board

    def get_element_delay(self, element: pcbnew.BOARD_CONNECTED_ITEM) -> float:

        if type(element) == pcbnew.PCB_TRACK:
            return self.get_track_delay(element)
        elif type(element) == pcbnew.PCB_VIA:
            return self.get_via_delay(element)
        else:
            raise Exception("Unhandled element type: " + type(element))

if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("Usage: gen_flytimes.py <kicad_pcb> <filename> <net_prefix> <sheet_name> (optional)")
        sys.exit(1)

    pcb_path = sys.argv[1]
    wb_name = sys.argv[2]
    net_prefix = sys.argv[3]

    wb = load_workbook(wb_name)

    if len(sys.argv) >= 4:
        sheet_name = sys.argv[4]
        ws = wb[sheet_name]
    else:
        ws = wb.active

    pcb = pcbnew.LoadBoard(pcb_path)

    flytools = FlyTools(pcb)

