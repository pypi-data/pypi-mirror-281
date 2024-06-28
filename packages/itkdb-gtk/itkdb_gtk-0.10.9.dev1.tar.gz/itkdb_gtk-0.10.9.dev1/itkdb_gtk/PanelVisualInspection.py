#!/usr/bin/env python3
"""PB/Hybrid panel Visual inspection GUI.."""
import json
import sys
import copy
from pathlib import Path

try:
    import itkdb_gtk

except ImportError:
    cwd = Path(__file__).parent.parent
    sys.path.append(cwd.as_posix())

from itkdb_gtk import dbGtkUtils, ITkDBlogin, ITkDButils
from itkdb_gtk.ShowComments import ShowComments
from itkdb_gtk.ShowDefects import ShowDefects
from itkdb_gtk.UploadTest import create_json_data_editor



import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GObject

HELP_LINK="https://itkdb-gtk.docs.cern.ch"

class TestJson(GObject.Object):
    """To store test JSOn."""
    __gtype_name__ = "TestJson"

    def __init__(self, js=None):
        super().__init__()
        self.js = copy.deepcopy(js)

    def set_js(self, js):
        """SEts the dictionary"""
        self.js = copy.deepcopy(js)


class PanelVisualInspection(dbGtkUtils.ITkDBWindow):
    """PB/Hybryd panel visual inspection GUI."""
    SN, PASSED, F_NAME, F_PATH, TEST_J, ALL = range(6)

    def __init__(self, session, title="PanelVisualInspection", help=HELP_LINK):
        super().__init__(title="ITkDB Dashboard",
                         session=session,
                         show_search="Find object with given SN.",
                         help=help)

        self.institute = "IFIC"
        # action button in header
        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="document-send-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        button.set_tooltip_text("Click to upload ALL tests.")
        button.connect("clicked", self.upload_tests)
        self.hb.pack_end(button)

        grid = Gtk.Grid(column_spacing=5, row_spacing=1)
        self.mainBox.pack_start(grid, False, False, 5)

        irow = 0
        receiver = self.create_institute_combo()
        receiver.connect("changed", self.on_institute)
        receiver.set_tooltip_text("Select the Institute making the test.")
        dbGtkUtils.set_combo_iter(receiver, self.institute)
        grid.attach(Gtk.Label(label="Institute"), 0, irow, 1, 1)
        grid.attach(receiver, 1, irow, 1, 1)

        irow += 1
        lbl = Gtk.Label(label="Serial Number")
        lbl.set_xalign(0)
        grid.attach(lbl, 0, irow, 1, 1)

        self.SN = dbGtkUtils.TextEntry(small=True)
        self.SN.connect("text_changed", self.SN_ready)
        self.SN.widget.set_tooltip_text("Enter SN of PWD or Hybrid panel.")
        grid.attach(self.SN.widget, 1, irow, 1, 1)

        self.panel_type = Gtk.Label(label="")
        grid.attach(self.panel_type, 2, irow, 1, 1)

        irow += 1
        lbl = Gtk.Label(label="Date")
        lbl.set_xalign(0)
        grid.attach(lbl, 0, irow, 1, 1)
        
        self.date = dbGtkUtils.TextEntry(small=True)
        grid.attach(self.date.widget, 1, irow, 1, 1)
        self.date.entry.set_text(ITkDButils.get_db_date())
        self.date.connect("text_changed", self.new_date)

        # Paned object
        paned = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
        paned.set_size_request(-1, 200)
        self.mainBox.pack_start(paned, True, True, 5)

        # the list of attachments
        tree_view = self.create_tree_view()
        paned.add1(tree_view)

        # The text view
        paned.add2(self.message_panel.frame)


        self.show_all()

        dbGtkUtils.setup_scanner(self.get_qrcode)

    def on_institute(self, combo):
        """A new recipient has been chosen."""
        name = self.get_institute_from_combo(combo)
        if name:
            self.institute = name

    def new_date(self, entry, value):
        """new date given at input."""
        d = dbGtkUtils.parse_date_as_string(value)
        if d is not None:
            self.date.set_text(d)


    def create_model(self):
        """Create tree view model."""
        return Gtk.ListStore(str, bool, str, str, TestJson)

    def create_tree_view(self, size=150):
        """Create the TreeView with the children."""
        model = self.create_model()
        self.tree = Gtk.TreeView(model=model)
        self.tree.connect("button-press-event", self.button_pressed)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(self.tree)
        scrolled.set_size_request(-1, size)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("SN", renderer, text=PanelVisualInspection.SN)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererToggle()
        renderer.set_property("activatable", True)
        renderer.set_property("radio", True)
        renderer.set_padding(5, 0)

        x, y = renderer.get_alignment()
        renderer.set_alignment(0, y)
        # renderer.set_property("inconsistent", True)
        renderer.connect("toggled", self.btn_toggled)

        column = Gtk.TreeViewColumn("Passed", renderer, active=PanelVisualInspection.PASSED)
        self.tree.append_column(column)


        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Image", renderer, text=PanelVisualInspection.F_NAME)
        self.tree.append_column(column)


        return scrolled

    def btn_toggled(self, renderer, path, *args):
        """Toggled."""
        model = self.tree.get_model()
        val = not model[path][PanelVisualInspection.PASSED]
        model[path][PanelVisualInspection.PASSED] = val


    def button_pressed(self, tree, event):
        """Button pressed on tree view."""
        # double click shows attachments
        if event.button == 1 and event.type == Gdk.EventType.DOUBLE_BUTTON_PRESS:
            self.write_message("This is a double click.\n")
            return

        if event.button != 3:
            return

        # Create popup menu
        select = self.tree.get_selection()
        model, iter = select.get_selected()
        values = None
        if iter:
            values = model[iter]

        if not iter:
            P = tree.get_path_at_pos(event.x, event.y)
            if P:
                print(P[0].to_string())
                iter = model.get_iter(P[0])
                values = model[iter]

        if not values:
            return

        menu = Gtk.Menu()

        item_show = Gtk.MenuItem(label="Upload Image")
        item_show.connect("activate", self.on_upload_image, (model, iter, values))
        menu.append(item_show)

        item_show_json = Gtk.MenuItem(label="Show JSOn")
        item_show_json.connect("activate", self.on_show_json, (model, iter, values))
        menu.append(item_show_json)

        item_show_com = Gtk.MenuItem(label="Edit Comments")
        item_show_com.connect("activate", self.on_show_comments, (model, iter, values))
        menu.append(item_show_com)

        item_show_def = Gtk.MenuItem(label="Edit Defects")
        item_show_def.connect("activate", self.on_show_defects, (model, iter, values))
        menu.append(item_show_def)

        menu.show_all()
        menu.popup_at_pointer(event)

    def on_upload_image(self, item, data):
        """Choose file."""
        fdlg = Gtk.FileChooserNative(action=Gtk.FileChooserAction.OPEN, accept_label="Select")
        response = fdlg.run()
        if response == Gtk.ResponseType.ACCEPT:
            ifiles = [ipath for ipath in fdlg.get_filenames()]
            if len(ifiles)<1:
                return

            if len(ifiles) > 1:
                dbGtkUtils.complain("More than one file selected","Choosing first.")

            fnam = ifiles[0]
            model, iter, val = data
            model.set_value(iter, PanelVisualInspection.F_PATH, fnam)
            model.set_value(iter, PanelVisualInspection.F_NAME, Path(fnam).name)


        self.write_message("Upload image\n")


    def on_show_json(self, item, data):
        """Test JSon."""
        model, iter, val = data
        payload = val[PanelVisualInspection.TEST_J].js
        value, dlg = create_json_data_editor(payload)
        rc = dlg.run()
        if rc == Gtk.ResponseType.OK:
            payload = value.values
            model.set_value(iter, PanelVisualInspection.TEST_J, TestJson(payload))

        dlg.hide()
        dlg.destroy()

    def on_show_comments(self, item, data):
        """Show comments"""
        model, iter, val = data
        js = val[PanelVisualInspection.TEST_J].js
        SC = ShowComments("Test Comments", js["comments"], self)
        rc = SC.run()
        if rc == Gtk.ResponseType.OK:
            js["comments"] = SC.comments
            model.set_value(iter, PanelVisualInspection.TEST_J, TestJson(js))

        SC.hide()
        SC.destroy()

    def on_show_defects(self, item, data):
        """Show comments"""
        model, iter, val = data
        js = val[PanelVisualInspection.TEST_J].js
        SD = ShowDefects("Test Defects", js["defects"], self)
        rc = SD.run()
        if rc == Gtk.ResponseType.OK:
            js["defects"] = SD.defects
            model.set_value(iter, PanelVisualInspection.TEST_J, TestJson(js))

        SD.hide()
        SD.destroy()

    def SN_ready(self, *args):
        """SN is ready in the TextEnttry."""
        SN = self.SN.get_text()
        # GEt children.
        panel = ITkDButils.get_DB_component(self.session, SN)
        if panel is None:
            self.write_message(ITkDButils.get_db_response())
            return

        SN = panel["serialNumber"]
        args[0].set_text(SN)
        is_PWB = False
        defaults = {
            "institution": self.institute,
            "runNumber": "1",
            "date": self.date.get_text()
        }
        component_type = None
        test_code = None
        if "USED" in SN:
            # Powerboard Carrier
            if not SN[6].isdigit():
                dbGtkUtils.complain("Not a Powerboard Carrier",
                                    "{}: wrong SN for a powerboard carrier".format(SN))
                self.SN.widget.set_text("")
                return

            self.panel_type.set_text("PWB carrier")
            is_PWB = True
            component_type = "PWB"
            test_code = "PICTURE"

        elif "USET" in SN:
            # Hybrid test panel
            component_type = "HYBRID_TEST_PANEL"
            test_code = "VISUAL_INSPECTION_RECEPTION"

            if not SN[6].isdigit or int(SN[6])>5:
                dbGtkUtils.complain("Not a Hybrid Test Panel",
                                    "{}: wrong SN for a hybrid test panel".format(SN))
                self.SN.widget.set_text("")
                return

            self.panel_type.set_text("HYB test panel")

        else:
            dbGtkUtils.complain("Invalid SN.",
                "{}\nNot a PWB carrier not HYB test panel.".format(SN))
            self.SN.widget.set_text("")
            return

        # GEt children.
        skltn = ITkDButils.get_test_skeleton(self.session, component_type, test_code, defaults)
        model = self.create_model()
        for child in panel["children"]:
            if child["component"] is not None:
                child_SN = child["component"]["serialNumber"]
                skltn["component"] = child_SN
                model.append([child_SN, True, "", "", TestJson(skltn)])

        self.tree.set_model(model)


    def upload_tests(self, *args):
        """Upload the current test."""
        SN = self.SN.get_text()

        model = self.tree.get_model()
        iter = model.get_iter_first()
        n_items = 0
        while iter:
            values = model[iter]
            payload = values[PanelVisualInspection.TEST_J].js
            ifile = values[PanelVisualInspection.F_PATH]
            if len(ifile)>0:
                attachments = [ITkDButils.Attachment(ifile, "Image", "Image")]
            else:
                attachments = []

            rc = ITkDButils.upload_test(self.session, payload, attachments)
            if rc:
                ipos = rc.find("The following details may help:")
                msg = rc[ipos:]
                dbGtkUtils.complain("Failed uploading test {}-{}".format(payload["component"], payload["testType"]), msg)
                self.write_message(msg)

            else:
                self.write_message("Upload {}-{} successfull\n".format(payload["component"], payload["testType"]))

            n_items += 1
            iter = model.iter_next(iter)


    def get_qrcode(self, fd, state, reader):
        """Read SN from scanner."""
        txt = dbGtkUtils.scanner_get_line(reader)
        self.write_message("SN: {}\n".format(txt))
        self.SN_ready(txt, self.SN.widget)


def main():
    """Main entry."""
    # DB login
    dlg = ITkDBlogin.ITkDBlogin()
    client = dlg.get_client()
    if client is None:
        print("Could not connect to DB with provided credentials.")
        dlg.die()
        sys.exit()

    client.user_gui = dlg

    gTest = PanelVisualInspection(client)

    gTest.present()
    gTest.connect("destroy", Gtk.main_quit)
    try:
        Gtk.main()

    except KeyboardInterrupt:
        print("Arrrgggg!!!")

    dlg.die()

if __name__ == "__main__":
    main()