# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

# Based on https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01

import platform
from tkinter import Canvas

from customtkinter import CTkFrame, CTkScrollbar


class ScrollableFrame(CTkFrame):
    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = Canvas(
            self, borderwidth=0, background="#2A2D2E", highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, sticky="nswe")

        self.content = CTkFrame(self.canvas)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.content, anchor="nw"
        )
        self.content.grid_columnconfigure(0, weight=1)

        self.scrollbar = CTkScrollbar(self, command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, padx=5, pady=5, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # bind an event whenever the size of the content frame changes.
        self.content.bind("<Configure>", self.on_frame_configure)

        # bind an event whenever the size of the canvas frame changes.
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # bind wheel events when the cursor enters the control
        self.content.bind("<Enter>", self.on_enter)

        # unbind wheel events when the cursorl leaves the control
        self.content.bind("<Leave>", self.on_leave)

        # perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize
        self.on_frame_configure(None)

    def on_frame_configure(self, event) -> None:
        """Reset the scroll region to encompass the inner frame"""

        # whenever the size of the frame changes, alter the scroll region respectively.
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event) -> None:
        """Reset the canvas window to encompass inner frame when required"""

        # whenever the size of the canvas changes alter the window region respectively.
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def on_mouse_wheel(self, event) -> None:
        """Cross platform scroll wheel event"""
        if platform.system() == "Windows":
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform.system() == "Darwin":
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

    def on_enter(self, event) -> None:
        """Bind wheel events when the cursor enters the control"""
        if platform.system() == "Linux":
            self.canvas.bind_all("<Button-4>", self.on_mouse_wheel)
            self.canvas.bind_all("<Button-5>", self.on_mouse_wheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def on_leave(self, event) -> None:
        """Unbind wheel events when the cursor leaves the control"""
        if platform.system() == "Linux":
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")
