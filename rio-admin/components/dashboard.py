import rio
from ..lib.px_to_rem import px_to_rem
from ..styles.dashboard import *


class Dashboard(rio.Component):
    def build(self) -> rio.Component:
        self.users_count = len(self.session._app_server.sessions)

        return rio.Column(
            # Title
            rio.Text("Dashboard", style="heading1"),
            # Users Online Card
            rio.Card(
                rio.Column(
                    rio.Icon(
                        icon="material/person",
                        fill="primary",
                        min_width=px_to_rem(CARD_ICON_SIZE),
                        min_height=px_to_rem(CARD_ICON_SIZE),
                    ),
                    rio.Row(
                        rio.Icon(
                            'material/circle:fill',
                            min_width=px_to_rem(20),
                            min_height=px_to_rem(20),
                            fill='success',
                        ),
                        rio.Text(
                            f"{self.users_count} {'Users' if self.users_count > 1 else 'User'} Online",
                            style="heading3",
                        ),
                        spacing=px_to_rem(4),
                    ),
                    spacing=px_to_rem(CARD_SPACING),
                    margin_x=px_to_rem(CARD_MARGIN_X),
                    margin_y=px_to_rem(CARD_MARGIN_Y),
                )
            ),
            align_x=0,
            align_y=0,
            spacing=px_to_rem(CONTAINER_SPACING),
            margin_y=px_to_rem(CONTAINER_MARGIN_Y),
        )
