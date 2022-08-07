# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

# Based on https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01

import platform
from tkinter import Canvas

from customtkinter import CTkFrame, CTkScrollbar


class ScrollableFrame(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)  # create a frame (self)

        self.grid_rowconfigure(
            0, weight=1
        )  # make the frame expandable in the y direction
        self.grid_columnconfigure(
            0, weight=1
        )  # make the frame expandable in the x direction

        self.canvas = Canvas(
            self, borderwidth=0, background="#2A2D2E", highlightthickness=0
        )  # place canvas on self
        self.content = CTkFrame(
            self.canvas
        )  # place a frame on the canvas, this frame will hold the child widgets
        self.scrollbar = CTkScrollbar(
            self, command=self.canvas.yview
        )  # place a scrollbar on self
        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )  # attach scrollbar action to scroll of canvas

        self.scrollbar.grid(row=0, column=1, padx=5, pady=5, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")  # attach canvas to self
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.content,
            anchor="nw",  # add view port frame to canvas
            tags="self.viewPort",
        )

        self.content.bind(
            "<Configure>", self.on_frame_configure
        )  # bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind(
            "<Configure>", self.on_canvas_configure
        )  # bind an event whenever the size of the canvas frame changes.

        self.content.bind(
            "<Enter>", self.on_enter
        )  # bind wheel events when the cursor enters the control
        self.content.bind(
            "<Leave>", self.on_leave
        )  # unbind wheel events when the cursorl leaves the control

        self.on_frame_configure(
            None
        )  # perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def on_frame_configure(self, event) -> None:
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )  # whenever the size of the frame changes, alter the scroll region respectively.

    def on_canvas_configure(self, event) -> None:
        """Reset the canvas window to encompass inner frame when required"""
        canvas_width = event.width
        self.canvas.itemconfig(
            self.canvas_window, width=canvas_width
        )  # whenever the size of the canvas changes alter the window region respectively.

    def on_mouse_wheel(self, event) -> None:  # cross platform scroll wheel event
        if platform.system() == "Windows":
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform.system() == "Darwin":
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

    def on_enter(
        self, event
    ) -> None:  # bind wheel events when the cursor enters the control
        if platform.system() == "Linux":
            self.canvas.bind_all("<Button-4>", self.on_mouse_wheel)
            self.canvas.bind_all("<Button-5>", self.on_mouse_wheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def on_leave(
        self, event
    ) -> None:  # unbind wheel events when the cursorl leaves the control
        if platform.system() == "Linux":
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")
