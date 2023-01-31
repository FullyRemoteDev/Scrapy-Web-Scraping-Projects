import scrapy


def fifth(input_list):
    start = 0
    end = 5

    while end <= len(input_list):
        yield input_list[start:end]
        start += 5
        end += 5


class LeagueTableSpider(scrapy.Spider):
    name = 'league_table'
    start_urls = ['https://www.espn.com/football/table/_/league/UEFA.CHAMPIONS/season/2021']

    def parse(self, response):
        dt = {}

        team_rows = response.css('table')[0].css('tr')
        detail_rows = response.css('table')[1].css('tr')

        for group, group_detail in zip(
                fifth(team_rows),
                fifth(detail_rows)
        ):
            group_label = group[0].css('td span::text').get()

            dt[group_label] = {}

            for team, detail in zip(group[1:], group_detail[1:]):
                team_label = team.css('td span.hide-mobile a::text').get()
                table_details = detail.css('td span::text').getall()

                dt[group_label][team_label] = {
                    "Wins": table_details[1],
                    "Draws": table_details[2],
                    "Lose": table_details[3],
                    "Points": table_details[-1]
                }

        yield dt
