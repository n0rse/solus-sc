#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  This file is part of solus-sc
#
#  Copyright © 2014-2016 Ikey Doherty <ikey@solus-project.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#

from gi.repository import Gtk

ICON_MAPS = {
    "database": "office-database",
    "desktop": "user-desktop",
    "desktop.budgie": "start-here-solus",
    "desktop.core": "system-run",
    "desktop.gnome": "start-here-symbolic",
    "desktop.gnome.core": "system-devices-information",
    "desktop.gnome.doc": "folder-documents",
    "desktop.gtk": "gtk-dialog-info",
    "desktop.library": "emblem-shared-symbolic",
    "desktop.multimedia": "multimedia-volume-control",
    "desktop.qt": "qtconfig-qt4",
    "desktop.theme": "preferences-desktop-wallpaper",
    "editor": "x-office-calendar",
    "office": "x-office-spreadsheet",
}


class ScComponentButton(Gtk.Button):
    """ Manage the monotony of a button """

    component = None

    def __init__(self, db, component):
        Gtk.Button.__init__(self)

        self.component = component

        c_desc = str(component.localName)
        if component.name in ICON_MAPS:
            icon = ICON_MAPS[component.name]
        else:
            icon = "package-x-generic"
        image = Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.SMALL_TOOLBAR)
        image.set_halign(Gtk.Align.START)
        # image.set_pixel_size(64)

        label_box = Gtk.VBox(0)

        box = Gtk.HBox(0)
        box.pack_start(image, False, False, 0)
        image.set_property("margin-right", 10)
        label = Gtk.Label(c_desc)
        label.get_style_context().add_class("title")
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        label_box.pack_start(label, True, True, 0)
        box.pack_start(label_box, True, True, 0)
        # self.set_relief(Gtk.ReliefStyle.NONE)
        self.add(box)

        # count the components
        count = len(db.get_packages(component.name))
        info_label = Gtk.Label(str(count))
        info_label.set_halign(Gtk.Align.START)
        info_label.get_style_context().add_class("info-label")
        info_label.get_style_context().add_class("dim-label")
        # label_box.pack_start(info_label, False, False, 0)

        self.get_style_context().add_class("group-button")

class ScComponentsView(Gtk.EventBox):
    """ Main group view, i.e. "System", "Development", etc. """

    label = None
    flowbox = None
    owner = None

    def __init__(self, owner):
        Gtk.EventBox.__init__(self)
        self.owner = owner

        self.scroll = Gtk.ScrolledWindow(None, None)
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.add(self.scroll)

        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_property("margin-start", 40)
        self.flowbox.set_property("margin-end", 40)
        self.flowbox.set_property("margin-top", 20)
        self.flowbox.set_column_spacing(10)
        self.flowbox.set_row_spacing(10)
        self.flowbox.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.flowbox.set_valign(Gtk.Align.START)
        self.scroll.add(self.flowbox)

    def set_components(self, components):
        """ Update our view based on a given set of components """
        for widget in self.flowbox.get_children():
            widget.destroy()
        compdb = self.owner.basket.componentdb
        for comp in components:
            component = compdb.get_component(comp)
            btn = ScComponentButton(compdb, component)
            self.flowbox.add(btn)
            btn.show_all()
            print(component.name)
