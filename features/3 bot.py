bot = interactions.Client(token=input("Please enter your Bot-Token: "),
                          intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MEMBERS,
                          presence=interactions.ClientPresence(
                              activities=[interactions.PresenceActivity(
                                  name="/help",
                                  type=interactions.PresenceActivityType.WATCHING)],
                              status=interactions.StatusType.ONLINE
                          )
                          )