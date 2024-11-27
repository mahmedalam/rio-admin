import random
import rio
from ..utils import px_to_rem, get_country_from_ip

# Container
CONTAINER_SPACING = 32
CONTAINER_MARGIN_Y = 32

# Card
CARD_SPACING = 12
CARD_MARGIN_X = 24
CARD_MARGIN_Y = 20

# Card Icon
CARD_ICON_SIZE = 52


class Dashboard(rio.Component):
    """
    The Dashboard component is responsible for building a user interface that provides
    a summary of the online users and their geographical distribution.
    """

    def build(self) -> rio.Component:
        self.sessions = self.session._app_server.sessions
        self.users_count = len(self.sessions)
        self.users = {}

        for user in self.sessions:
            # For Test
            test_ips = ["103.209.79.0", "170.171.1.9", "103.177.248.0", "103.139.210.0"]
            ip = test_ips[random.randint(0, len(test_ips) - 1)]
            # ip = user.client_ip
            response = get_country_from_ip(ip)

            if response is None:
                key = "?:Unknown"

                if self.users.get(key) is None:
                    self.users[key] = [ip]
                else:
                    self.users[key].append(ip)

                continue

            country, city, flag = response
            key = f"{flag}:{country}, {city}"

            if self.users.get(key) is None:
                self.users[key] = [ip]
            else:
                self.users[key].append(ip)

        return rio.Column(
            # Title
            rio.Text("Dashboard", style="heading1", align_x=0.5),
            # Users Online Card
            rio.Card(
                rio.Column(
                    rio.Icon(
                        icon="material/person",
                        fill="primary",
                        min_width=px_to_rem(CARD_ICON_SIZE),
                        min_height=px_to_rem(CARD_ICON_SIZE),
                    ),
                    rio.Text(
                        f"{self.users_count} {'Users' if self.users_count > 1 else 'User'} Online",
                        style="heading3",
                        align_x=0.5,
                    ),
                    spacing=px_to_rem(CARD_SPACING),
                    margin_x=px_to_rem(CARD_MARGIN_X),
                    margin_y=px_to_rem(CARD_MARGIN_Y),
                )
            ),
            rio.Row(
                # Users From Country Card
                *[
                    rio.Card(
                        rio.Column(
                            rio.Html(
                                f"""
                                <div style="font-size: 72px">
                                {key.split(":")[0]}
                                </div>
                                """,
                                align_x=0.5,
                            ),
                            rio.Text(key.split(":")[1], style="heading3", align_x=0.5),
                            rio.Text(str(len(value)), align_x=0.5),
                            spacing=px_to_rem(CARD_SPACING),
                            margin_x=px_to_rem(CARD_MARGIN_X),
                            margin_y=px_to_rem(CARD_MARGIN_Y),
                        )
                    )
                    for key, value in self.users.items()
                ],
                align_x=0.5,
                align_y=0,
                spacing=px_to_rem(CONTAINER_SPACING),
                margin_y=px_to_rem(CONTAINER_MARGIN_Y),
            ),
            align_x=0,
            align_y=0,
            spacing=px_to_rem(CONTAINER_SPACING),
            margin_y=px_to_rem(CONTAINER_MARGIN_Y),
        )
