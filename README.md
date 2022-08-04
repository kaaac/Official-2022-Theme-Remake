# Official 2022 Theme Remake

This is Remake of Official Theme F1 2022 event results layout for Racing League Tools

## Installation

Unpack the .zip file in the Racing League Tools location

```
RacingLeagueTools/user/mods/
```

## Features

### Available render layouts:

- DriverStandings (driverStandings)
- Calendar (Calendar)
- QualResults (qualResults)
- RaceResults (raceResults)
- DriverStandings (SeasonProgressPositions)
- DriverStandings (SeasonProgressPoints)
- DriverStandings (SeasonProgressQualificationPositions)
- TeamStandings (SeasonTeamProgressPositions)
- TeamStandings (teamStandings)

Official renders of the session results do not always have information about the tires used during the session, so it is possible to disable their display.
Just edit file `official-2022-theme-remake/global/global_vars.json` by changing the values of each option from true to false:
```json
     "RenderQualiStints": "true",
     "RenderRaceStints": "true",
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
