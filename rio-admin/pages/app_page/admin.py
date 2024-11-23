from datetime import datetime, timezone
import functools
from pathlib import Path

import rio

from ...components import Dashboard
from ...lib.px_to_rem import px_to_rem
from ...constants.admin import *
from ...styles.admin import *
from ... import data_models
from ... import persistence


def guard(event: rio.GuardEvent) -> str | None:
    """
    A guard which only allows the user to access this page if they are not
    logged in yet. If the user is already logged in, the login page will be
    skipped and the user will be redirected to the home page instead.
    """
    # Check if the user is authenticated by looking for a user session
    try:
        event.session[data_models.AppUser]

    # User is not logged in, no redirection needed
    except KeyError:
        return None

    # User is logged in, redirect to the home page
    return None


@rio.page(
    name="Admin",
    url_segment="admin",
    guard=guard,
)
class AdminPage(rio.Component):
    active_tab: str = "Dashboard"

    def on_press_button(self, button_name: str) -> None:
        self.active_tab = button_name

    async def on_logout(self) -> None:
        user_session = self.session[data_models.UserSession]

        # Expire the session
        pers = self.session[persistence.Persistence]

        await pers.update_session_duration(
            user_session,
            new_valid_until=datetime.now(tz=timezone.utc),
        )

        # Detach everything from the session. This informs all components that
        # nobody is logged in.
        self.session.detach(data_models.AppUser)
        self.session.detach(data_models.UserSession)

        # Navigate to the login page to prevent the user being on a page that is
        # prohibited without being logged in.
        self.session.navigate_to("/")

    def build(self) -> rio.Component:
        print(self.session._app_server.sessions)

        return rio.Row(
            # Sidebar
            rio.Column(
                # Top Container
                rio.Row(
                    rio.Image(
                        Path(self.session.assets / "logo.png"),
                        fill_mode="fit",
                        align_x=0.5,
                        min_width=px_to_rem(SIDEBAR_LOGO_WIDTH),
                        min_height=px_to_rem(SIDEBAR_LOGO_HEIGHT),
                    ),
                ),
                # Main Buttons Container
                rio.Column(
                    *[
                        rio.Button(
                            button["name"],
                            icon=button["icon"],
                            shape="rounded",
                            style=(
                                "plain-text"
                                if button["name"] != self.active_tab
                                else "major"
                            ),
                            on_press=functools.partial(
                                self.on_press_button, button_name=button["name"]
                            ),
                        )
                        for button in SIDEBAR_MAIN_BUTTONS
                    ],
                    spacing=px_to_rem(SIDEBAR_BUTTONS_CONTAINER_SPACING),
                ),
                # Bottom Buttons Container
                rio.Column(
                    *[
                        rio.Button(
                            button["name"],
                            icon=button["icon"],
                            shape="rounded",
                            style=(
                                "plain-text"
                                if button["name"] != self.active_tab
                                else "major"
                            ),
                            on_press=functools.partial(
                                self.on_press_button, button_name=button["name"]
                            ),
                        )
                        for button in SIDEBAR_BOTTOM_BUTTONS
                    ],
                    rio.Button(
                        "Logout",
                        icon="material/logout",
                        shape="rounded",
                        style="plain-text",
                        on_press=self.on_logout,
                    ),
                    spacing=px_to_rem(SIDEBAR_BUTTONS_CONTAINER_SPACING),
                    align_y=1,
                ),
                min_width=px_to_rem(SIDEBAR_WIDTH),
                align_x=0,
                align_y=0,
                margin_x=px_to_rem(SIDEBAR_MARGIN_X),
                margin_y=px_to_rem(SIDEBAR_MARGIN_Y),
                spacing=px_to_rem(SIDEBAR_SPACING),
                grow_y=True,
            ),
            # Main content
            rio.Column(
                (
                    Dashboard()
                    if self.active_tab == "Dashboard"
                    else rio.Text(text=self.active_tab)
                ),
            ),
        )
