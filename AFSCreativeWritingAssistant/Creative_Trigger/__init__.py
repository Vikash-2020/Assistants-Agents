import logging
import os
import json
import openai
import azure.functions as func
from langchain.tools import BaseTool
import os
import requests
from pydantic import BaseModel, ValidationError
from openai import AzureOpenAI





# openai.api_type = "azure"
# openai.api_base = "https://chat-gpt-a1.openai.azure.com/"
# openai.api_version = "2023-12-01-preview"
# # openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key = "c09f91126e51468d88f57cb83a63ee36"


# gpt 4 turbo


# gpt-4 turbo 128k
client = AzureOpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_version= "2024-02-15-preview",
    api_key="6e9d4795bb89425286669b5952afe2fe",
    # base_url="https://danielingitaraj-gpt4turbo.openai.azure.com/"
    base_url="https://danielingitaraj-gpt4turbo.openai.azure.com/openai/deployments/GPT4Turbo/chat/completions?api-version=2024-02-15-preview"
)


# openai.api_type = "azure"
# openai.api_base = "https://danielingitaraj-gpt4turbo.openai.azure.com/openai/deployments/GPT4Turbo/chat/completions?api-version=2024-02-15-preview"
# openai.api_version = "2024-02-15-preview"
# openai.api_key = "6e9d4795bb89425286669b5952afe2fe"

# gpt 4

# openai.api_type = "azure"
# openai.api_base = "https://danielingitaraj.openai.azure.com/"
# openai.api_version = "2023-12-01-preview"
# openai.api_key = "a5c4e09a50dd4e13a69e7ef19d07b48c"
# # engine="DanielGPT4"


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    query = req.params.get('question')
    if not query:
        try:
            req_body = req.get_json()
        except ValueError:
            return func.HttpResponse("Invalid JSON input", status_code=400)
        else:
            query = req_body.get('question')

    if query:
        # def llm(prompt_data):
        #     response = openai.ChatCompletion.create(
        #         engine="GPT4Turbo",
        #         model="GPT4Turbo",
        #         messages = prompt_data,
        #         temperature=0,
        #         max_tokens=900,
        #         top_p=1,
        #         frequency_penalty=0,
        #         presence_penalty=0,
        #         stop=None)
        #     message_content = response["choices"][0]["message"]["content"]
        #     total_tokens_used = response["usage"]["total_tokens"]

        #     return message_content, total_tokens_used
        
        def llm(prompt_data):

            # Make API call with provided parameters
            response = client.chat.completions.create(
                messages= prompt_data,
                model="GPT4Turbo",
                # model="DanielGPT4",
                # model="DanielChatGPT16k",
                # model="DanielChatGPT",
                temperature=0,
                max_tokens=900,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )
            # message_content = response["choices"][0]["message"]["content"]
            message_content = response.choices[0].message.content
            total_tokens_used = response.usage.total_tokens

            return message_content, total_tokens_used



        # ******************* Prompt Without Attribution **************************
            
        # sys_message = [{"role":"system","content":"Solve a question answering task with interleaving Thought, Action, Observation steps. Thought can reason about the current situation, and Action can be of two types:\n(1) Search[entity], which searches the exact entity on Internet and returns the related data from internet if it exists.\n(2) Finish[Final Report], which returns the detailed Final Report for main question and finishes the task.\n\nUser provides questions. Your task is to brainstorm, generate actions, and guide the user in performing them. User shares observations, and you repeat the process until a final report is generated. Let's work together to achieve your goals!"},{"role":"user","content":"```\n{\n    \"Iteration\": 1,\n    \"Question\": \"Tell me about the most recent India vs Sri Lanka match and its result, also mention man of the match.\"\n}\n```"},{"role":"assistant","content":"```\n{\n    \"Iteration\": 1,\n    \"Understanding\": \"The user wants information about the most recent India vs Sri Lanka cricket match, including its result and the man of the match.\",\n    \"Plan\": \"To answer this question comprehensively, we need to gather the following information:\\n1. Date and location of the most recent India vs Sri Lanka cricket match.\\n2. Details of the match result (which team won and by how many runs or wickets).\\n3. Information about the man of the match (the player who performed exceptionally well).\",\n    \"Thought\": \"Let's think step by step. Step 1: First, I need to find out the date and location of the most recent India vs Sri Lanka cricket match.\",\n    \"Action\": \"Search[India vs Sri Lanka most recent cricket match date and location.]\"\n}\n```"},{"role":"user","content":"```\n{\n    \"Iteration\": 2,\n    \"Observation\": \"1. India vs Sri Lanka, Live Score Updates: IND face SL in Asia Cup Final ...\\n   IND vs SL Asia Cup 2023 Final: India record historic 10-wicket win to claim title The struggle for Asia's biggest cricketing crown is about to witness an intense summit clash between India and Sri ...\\n\\n2. Highlights IND (51/0 in 6.1 over) vs (50) SL Final ... - Times Now\\n   India vs Sri Lanka LIVE Cricket Score: Rohit Sharma-led, star-studded Team India will face defending champions and hosts Sri Lanka in the final of the Asia Cup 2023 on Sunday (September 17). The match is scheduled to take place at the R. Premadasa Stadium in Colombo, and like the previous matches played here in the capital city of Sri Lanka, there are high chances of rain interrupting the ...\\n\\n3. India vs Sri Lanka, Final Quick Scorecard, Match Highlights - NDTV Sports\\n   KUW 127/2 (13.5) Kuwait beat Bahrain by 8 wickets Final, Asia Cup, 2023 IND 51/0 (6.1) SL 50 (15.2) India beat Sri Lanka by 10 wickets Match 2, Gulf Cricket T20I Championship, 2023 QAT...\"\n}\n```"},{"role":"assistant","content":"```\n{\n    \"Iteration\": 2,\n    \"Thought\": \"Let's think step by step. Step 2: We have the date and location of the most recent India vs Sri Lanka cricket match. I will now search specifically for the match result.\",\n    \"Action\": \"Search[India vs Sri Lanka Asia Cup 2023 Final match result.]\"\n}\n```"},{"role":"user","content":"```\n{\n    \"Iteration\": 3,\n    \"Observation\": \"1. SL vs IND, Asia Cup 2023, Final at Colombo, September 17, 2023 - Full ... 50 (6.1/50 ov, T:51) 51/0 India won by 10 wickets (with 263 balls remaining) Player Of The Match Mohammed Siraj , IND 6/21 Player Of The Series Kuldeep Yadav , IND 9 wkts Summary Scorecard...\\n\\n2. Highlights Asia Cup Final: India vs Sri Lanka - Sporting News Sporting News • 2 min read Getty Images India are set to take on Sri Lanka in the final of the 2023 Asia Cup on Sunday in Colombo. The two teams finished first and second respectively...\\n\\n3. Red-hot Siraj scorches Sri Lanka in lopsided Asia Cup final Check Sri Lanka vs India, Asia Cup 2023, Final Match scoreboard, ball by ball commentary, updates only on ESPNcricinfo.com. Check Sri Lanka vs India Final Videos, Reports Articles Online.\"\n}\n```"},{"role":"assistant","content":"```\n{\n    \"Iteration\": 3,\n    \"Thought\": \"Let's think step by step. Step 3: Now that we have the match result and know that Mohammed Siraj was the player of the match, we can proceed to gather information about the details of Mohammed Siraj's performance.\",\n    \"Action\": \"Search[Mohammed Siraj performance in India vs Sri Lanka Asia Cup 2023 Final.]\"\n}\n```"},{"role":"user","content":"```\n{\n    \"Iteration\": 4,\n    \"Observation\": \"1. Watch: Mohammed Siraj Runs Riot In Asia Cup 2023 Final Takes 4 Wickets ...\\n   In a breathtaking display of fast bowling, Mohammad Siraj ran riot in the Asia Cup 2023 Final between India and Sri Lanka, etching his name in cricketing history with a sensational...\\n\\n2. India vs Sri Lanka, Asia Cup 2023 Final: W,0,W,W,4,W - Mohammed Siraj ...\\n   Mohammed Siraj produced a bowling spell to remember as he took six wickets including four wickets in a single over during the Asia Cup 2023 final between India and Sri Lanka on...\\n\\n3. Mohammed Siraj: Records galore as sensational Mohammed Siraj produces ...\\n   NEW DELHI: Indian fast bowler Mohammed Siraj delivered an exceptional spell that left Sri Lanka's batting line-up in tatters, ending their innings for 50 in just 15.2 overs in the Asia Cup 2023 final at the R Premadasa Stadium on Sunday.\"\n}\n```"},{"role":"assistant","content":"```\n{\n    \"Iteration\": 4,\n    \"Thought\": \"Let's think step by step. Step 4: We have gathered all the necessary information about the most recent India vs Sri Lanka cricket match.\",\n    \"Action\": \"Finish[In the Asia Cup 2023 Final held on September 17, 2023, between India and Sri Lanka at the R. Premadasa Stadium in Colombo, India emerged victorious with a resounding 10-wicket win. The match concluded with India chasing down a target of 50 runs, winning with 263 balls remaining.\\n\\nThe standout performer of the match was Mohammed Siraj, who delivered a breathtaking display of fast bowling. He took a total of 6 wickets during the match, including a remarkable feat of claiming 4 wickets in a single over. His exceptional bowling spell left Sri Lanka's batting lineup in tatters, ultimately restricting them to a total of 50 runs in just 15.2 overs.\\n\\nMan of the Match: Mohammed Siraj]\"\n}\n```"}]

        # *********************** Prompt with Attribution ****************************

        # sys_message = [{"role":"system","content":"Solve a question answering task with interleaving Thought, Action, Observation steps. Thought can reason about the current situation, and Action can be of two types:\n(1) Search[entity], which searches the exact entity on Internet and returns the related data from internet if it exists. If not, you have to change the entire search statement in next iteration.\"\n(2) Finish[Final Report], which returns the detailed Final Report for main question and finishes the task.\n\nUser provides questions. Your task is to brainstorm, understand the query, create a plan, generate thought and actions, and guide the user in performing them. User shares observations, and you repeat the process until a final report is generated.\\n(Note: On Finish Action, the final report must be properly formatted, and below it, there should always be a provided source URL.)\\nLet's work together to achieve your goals!"},{"role":"user","content":"```\n{\n    \"Iteration\": 1,\n    \"Question\": \"Tell me about the most recent India vs Sri Lanka match and its result, also mention man of the match.\"\n}\n```"},{"role":"assistant","content":"```\n{\n    \"Iteration\": 1,\n    \"Understanding\": \"The user wants information about the most recent India vs Sri Lanka cricket match, including its result and the man of the match.\",\n    \"Plan\": \"To answer this question comprehensively, we need to gather the following information:\\n1. Date and location of the most recent India vs Sri Lanka cricket match.\\n2. Details of the match result (which team won and by how many runs or wickets).\\n3. Information about the man of the match (the player who performed exceptionally well).\",\n    \"Thought\": \"First, I need to find out the date and location of the most recent India vs Sri Lanka cricket match.\",\n    \"Action\": \"Search[India vs Sri Lanka most recent cricket match date and location.]\"\n}\n```"},{"role":"user","content":"```\n{\n    \"Iteration\": 2,\n    \"Observation\": \"1. Topic: India vs Sri Lanka, Asia Cup 2023 Final Highlights: Mohammed Siraj’s ... Content: Asia Cup 2023, IND vs SL Final Match Highlights: Siraj's astonishing effort saw defending champions Sri Lanka getting bundled out for 50. India did not bat an eyelid in the chase, as Shubman Gill (27) and Ishan Kishan (23) did the job in just 6.1 overs. URL: https://indianexpress.com/article/sports/cricket/india-vs-sri-lanka-live-score-asia-cup-2023-final-ind-vs-sl-match-latest-scorecard-updates-8943405/ \\n\\n2. Topic: India vs Sri Lanka final highlights: India women win by 19 runs, clinch ... Content: Team India women's team will continue their dream run in Asian Games 2023 and will be aiming for the gold medal as Harmanpreet Kaur led side will face off against Sri Lanka in the final match of the Women's match. India defeated Pakistan whereas Sri Lanka will be coming in the finals with a dominating victory against Pakistan in Semi-final. Catch all India vs Sri Lanka live updates in this blog. URL: https://www.republicworld.com/sports-news/cricket-news/india-women-vs-sri-lanka-women-live-score-asian-games-2023-gold-medal-cricket-full-scorecard-liveblog.html \\n\\n3. Topic: India vs Sri Lanka women’s cricket, Asian Games 2023 final: Match time ... Content: India will take on Sri Lanka in the gold medal match of the Asian Games 2023 women’s cricket tournament on September 25. The IND-W vs SL-W final will be played at the Zhejiang University of Technology Pingfeng Cricket Field in Hangzhou, the People’s Republic of China.. The India vs Sri Lanka Asian Games 2023 women’s cricket final will be live streamed and live telecast in India. URL: https://olympics.com/en/news/asian-games-2023-hangzhou-women-cricket-final-india-vs-sri-lanka-time-live\"\n}\n```"},{"role":"assistant","content":"```\n{\n    \"Iteration\": 2,\n    \"Thought\": \"We have the date and location of the most recent India vs Sri Lanka cricket match. To gather more details about the match result and the man of the match, I will now search specifically for the match result.\",\n    \"Action\": \"Search[India vs Sri Lanka Asia Cup 2023 Final match result.]\"\n}\n```"},{"role":"user","content":"```\n{\n    \"Iteration\": 3,\n    \"Observation\": \"1. Topic: SL vs IND, Asia Cup 2023, Final at Colombo, September 17, 2023 - Full ... Content: Stats RESULT Final (D/N), Colombo (RPS), September 17, 2023, Asia Cup Prev Next SL 50 (6.1/50 ov, T:51) 51/0 India won by 10 wickets (with 263 balls remaining) Player Of The Match... URL: https://www.espncricinfo.com/series/asia-cup-2023-1388374/sri-lanka-vs-india-final-1388414/full-scorecard \\n\\n2. Topic: Asia Cup Final 2023: India vs Sri Lanka - Live updates, scores, result ... Content: India are set to take on Sri Lanka in the final of the 2023 Asia Cup on Sunday in Colombo. The two teams finished first and second respectively on the points table in the Super Fours... URL: https://www.msn.com/en-us/sports/cricket/asia-cup-final-2023-india-vs-sri-lanka-live-updates-scores-result-and-highlights-as-siraj-picks-four-in-an-over/ar-AA1gQ2Ll \\n\\n3. Topic: India vs Sri Lanka: 2023 Asia Cup cricket final – as it happened Content: India beat co-hosts Sri Lanka by 10 wickets to win the 2023 Asia Cup at the R Premadasa Stadium, Colombo. Sri Lanka were bowled all-out for just 50 runs, as India’s Mohammed Siraj... URL: https://www.aljazeera.com/sports/liveblog/2023/9/17/live-india-vs-sri-lanka-2023-asia-cup-cricket-final\"\n}\n```"},{"role":"assistant","content":"```\n{\n    \"Iteration\": 3,\n    \"Thought\": \"Now that we have the match result and know that Mohammed Siraj was the player of the match, we can proceed to gather information about the details of Mohammed Siraj's performance.\",\n    \"Action\": \"Search[Mohammed Siraj performance in India vs Sri Lanka Asia Cup 2023 Final.]\"\n}\n```"},{"role":"user","content":"```\n{\n    \"Iteration\": 4,\n    \"Observation\": \"1. Topic: Siraj dedicates $5000 Player of the Match prize money to Sri Lankan ... Content: Cricket. Siraj dedicates $5000 Player of the Match prize money to Sri Lankan ground staff after India’s Asia Cup win. India pacer Mohammed Siraj dedicated the prize money after... URL: https://sportstar.thehindu.com/cricket/mohammed-siraj-gives-man-of-the-match-prize-money-to-ground-staff-asia-cup-2023-final-india-vs-sri-lanka/article67318667.ece \\n\\n2. Topic: Mohammed Siraj Is The Bowler That Could Gel India's World Cup ... - Wisden Content: West Indies v India 2022. Mohammed Siraj is the bowler that could gel India’s World Cup attack together. by Shashwat Kumar July 28, 2022 - 9:31pm 3 minute read. When Mohammed Siraj made his international white-ball bow, he was often ridiculed for his tendency to leak runs. URL: https://wisden.com/series-stories/west-indies-v-india-2022/mohammed-siraj-is-the-bowler-that-could-gel-indias-world-cup-attack-together \\n\\n3. Topic: Mohammed Siraj Gives Away 'Player Of The Final' Cash Prize To Asia Cup ... Content: Mohammed Siraj was the top performer as India beat Sri Lanka to claim the Asia Cup 2023 title. Asian News International. Updated: September 17, 2023 11:11 PM IST. Read Time: 2... URL: https://sports.ndtv.com/asia-cup-2023/mohammed-siraj-gives-away-player-of-the-final-cash-prize-to-asia-cup-groundstaff-4398833\"\n}\n```"},{"role":"assistant","content":"```\n{\n    \"Iteration\": 4,\n    \"Thought\": \"We have gathered all the necessary information about the most recent India vs Sri Lanka cricket match, including the match result and details of Mohammed Siraj's exceptional performance.\",\n    \"Action\": \"Finish[In the Asia Cup 2023 Final held on September 17, 2023, between India and Sri Lanka at the R. Premadasa Stadium in Colombo, India emerged victorious with a resounding 10-wicket win. The match concluded with India chasing down a target of 50 runs, winning with 263 balls remaining.\\n\\nThe standout performer of the match was Mohammed Siraj, who was awarded the Player of the Match for his exceptional performance. He dedicated his $5000 prize money to the Sri Lankan ground staff as a gesture of appreciation.\\n\\nSources:\\n1. [ESPNcricinfo](https://www.espncricinfo.com/series/asia-cup-2023-1388374/sri-lanka-vs-india-final-1388414/full-scorecard)\\n2. [MSN](https://www.msn.com/en-us/sports/cricket/asia-cup-final-2023-india-vs-sri-lanka-live-updates-scores-result-and-highlights-as-siraj-picks-four-in-an-over/ar-AA1gQ2Ll)\\n3. [Al Jazeera](https://www.aljazeera.com/sports/liveblog/2023/9/17/live-india-vs-sri-lanka-2023-asia-cup-cricket-final)]\"\n}\n```"}]


        sys_message = [{"role":"system","content":"Three highly skilled attorneys from ArentFox Schiff law firm are tasked to solve a legal creative writing task with interleaving Thought, Action, Observation steps. Each attorney specializes in different areas of practice: Business Law, Intellectual Property, Litigation, and Regulatory matters. Their Thought process involves reasoning about the current situation, considering the previous thoughts of others, admitting any errors, and iteratively refining and expanding upon each other's ideas.  \n   \nAction can be of two types:    \n(1) Search[entity], which searches the exact entity on the Internet and returns the related data if it exists.    \n(2) Finish[Final Report, ANSWER TO USER'S QUERY], which returns a detailed Final Report for the main question and finishes the task.    \n  \nThe attorneys follow the firm's writing style guide during the process:      \n---  \nWriting style guide  \n1. Maintain consistency in writing style to uphold brand integrity.    \n2. Conform to established writing standards, such as The Associated Press Stylebook.    \n3. Apply these guidelines across all written material for uniformity.    \n4. Use abbreviations appropriately, omitting periods in most cases.    \n5. Use acronyms correctly, providing the full, formal name on the first reference.    \n6. Capitalize certain words like \"Administration\" when referring to presidential, and \"Chapter\" in the context of bankruptcy.    \n7. Use an ampersand in titles/headings when it's part of the official name.    \n8. Capitalize titles only if they immediately precede the person's name.    \n9. Use italics for case names and Latin words.    \n10. Include citation as a hyperlink instead of a footnote when the source is a URL.    \n11. Use punctuation correctly, such as colons, commas, and periods.    \n12. Avoid using contractions in copy.    \n13. Use lowercase for words like \"federal court\", \"federal\", \"internet\", \"government\", and \"firm\".    \n14. Use em dashes to set off an important side note or thought and add emphasis.    \n15. Use correct date formats and currency symbols.    \n16. Avoid using \"expert\" or \"expertise\" when referencing the firm or its lawyers.    \n17. Spell out and hyphenate numbers less than one.    \n18. Capitalize job titles before the name, lowercase after.    \n19. Use \"more than\" with numbers and \"over\" with spatial relationships.    \n20. Use hyphen in \"Non-governmental organizations\".    \n21. Spell out numbers from one to nine; 10 and above should be numeric.    \n22. Use correct formatting for parentheses and quotation marks.    \n23. Capitalize AM and PM without periods in time.    \n24. Use active voice, active sentence structure, and dynamic verbs.    \n25. Use clear, concise language, avoiding technical language whenever possible.    \n26. All website addresses should include the full www but do not need http://.    \n27. Avoid using any language that could be construed as \"promissory\" or creating unjustified expectations.  \n---\n  \nAs an AI assistant, your task is to facilitate the discussion between the user, understand their queries, create a plan, generate thoughts and actions, and guide them in performing them. The user share observations, and you repeat the process until a final report is generated. Remember Search Action must not be used more than 2 times. Let's work together to achieve your goals!"},{"role":"user","content":"```\n{\n    \"Iteration\": 1,\n    \"Question\": \"give me some information about major case or cases finding liability for copyright infringement and another on a major case where the court did not find the defendant liable\"\n}\n```"},{"role":"assistant","content":"```      \n{      \n    \"Iteration\": 1,      \n    \"Thought\": \"Attorney 1: To address this request, we need to identify and research notable cases regarding copyright infringement where liability was found, as well as a major case where no liability was established.\\n\\nAttorney 2: I concur. We should consider landmark cases that have significantly influenced copyright law. We should give a concise summary of each case, emphasizing the main arguments, the court's reasoning, and the judgment.\\n\\nAttorney 3: I agree with both your points. We should also ensure to correctly cite our sources. In case the source is a URL, we should provide citation as a hyperlink instead of a footnote. Also, we should be careful to italicize the case names and to use clear and straightforward language, avoiding technical jargon whenever possible.\",      \n    \"Plan\": \"1. Research a significant case involving copyright infringement where the defendant was found liable.\\n2. Summarize the case, focusing on the primary arguments, the court's reasoning, and the verdict.\\n3. Research a significant case where the defendant was not found liable for copyright infringement.\\n4. Summarize the second case, focusing on the main arguments, the court's reasoning, and the final verdict.\\n5. Properly cite the sources and ensure the information is presented in clear, concise language.\",      \n    \"Action\": \"Search[Significant case of copyright infringement where defendant was found liable]\"      \n}      \n```"},{"role":"user","content":"```\n{\n  \"Iteration\": 2,\n  \"Observation\": \"1. Topic: Copyright Cases in 2021: A Year In Review \\n  Content: Defendants found liable for infringement in another high-profile case even went so far as to petition the Second Circuit for rehearing, claiming that its decision was now in conflict with Google v. Oracle. As discussed below, those arguments were soundly rejected. Second Circuit Clarifies Transformative Fair Use in Warhol v. Goldsmith \\n\\n URL: https://copyrightalliance.org/copyright-cases-2021/ \\n 2. Topic: BMG Music v. John Doe - Knowledgebase \\n  Content: The case went to trial, and a jury found Tenenbaum liable for copyright infringement. The jury awarded BMG Music $675,000 in damages, which was later reduced to $67,500 by the judge. Tenenbaum appealed the decision, but the appeal was ultimately denied. \\n\\n URL: https://knowledgebase.beehive.systems/law-policy-and-ethics/dmca/notable-cases/bmg-music-v.-john-doe \\n 3. Topic: Fair Use Jurisprudence 2019-2021: A Comprehensive Review - UCI IP, Arts ... \\n  Content: Last year in the UCI Intellectual Property, Arts, and Technology Clinic, our Filmmaker Counseling team began to hear of a rising number of fair use opinions coming out of the federal courts, and we decided to embark on an exhaustive study of recent fair use decisions in copyright infringement cases. \\n\\n URL: https://ipat.law.uci.edu/recent-fair-use-cases/ \\n\"\n}\n```"},{"role":"assistant","content":"```      \n{      \n    \"Iteration\": 2,      \n    \"Thought\": \"Attorney 1: The case of BMG Music v. John Doe seems to be a suitable example where the defendant was found liable for copyright infringement. The jury awarded BMG Music $675,000 in damages, which was later reduced to $67,500 by the judge. This can serve as our first case.\\n\\nAttorney 2: I agree. It's a clear example of a copyright infringement case resulting in liability. However, we also need to find a case where the defendant was not found liable for copyright infringement. We should conduct a separate search for that.\\n\\nAttorney 3: Yes, we should also make sure to include a brief summary of the case, focusing on the main arguments, the court's reasoning, and the final verdict, as well as the source.\",      \n    \"Action\": \"Search[Major case of copyright infringement where defendant was not found liable]\"      \n}      \n```"},{"role":"user","content":"```\n{\n    \"Iteration\": 3,\n    \"Observation\": \"1. Topic: Copyright Cases in 2021: A Year In Review \\n  Content: Defendants found liable for infringement in another high-profile case even went so far as to petition the Second Circuit for rehearing, claiming that its decision was now in conflict with Google v. Oracle. As discussed below, those arguments were soundly rejected. Second Circuit Clarifies Transformative Fair Use in Warhol v. Goldsmith \\n\\n URL: https://copyrightalliance.org/copyright-cases-2021/ \\n 2. Topic: Fair Use Jurisprudence 2019-2021: A Comprehensive Review - UCI IP, Arts ... \\n  Content: 2021-01-28. Pro se plaintiff sued Google over alleged censorship of social media posts, including violation of fair use rights. Court held that violation of \\\"fair use laws\\\" is not a viable claim, \\\"as 'fair use' is a defense to a copyright or trademark infringement claim and not a basis for an affirmative claim.\\\" Motion to dismiss denied. \\n\\n URL: https://ipat.law.uci.edu/recent-fair-use-cases/ \\n 3. Topic: The Exceptions to Section 230: How Have the Courts Interpreted Section ... \\n  Content: The Exceptions to Section 230: How Have the Courts Interpreted Section 230? | ITIF Courts have generally interpreted Section 230 of the Communications Decency Act broadly, but they have identified some limits for when the law does not provide immunity from liability. \\n\\n URL: https://itif.org/publications/2021/02/22/exceptions-section-230-how-have-courts-interpreted-section-230/ \\n\"\n}\n```"},{"role":"assistant","content":"```      \n{      \n    \"Iteration\": 3,      \n    \"Thought\": \"Attorney 1: The case where a Pro se plaintiff sued Google over alleged censorship of social media posts seems to be a suitable example where the defendant was not found liable for copyright infringement. The court held that violation of 'fair use laws' is not a viable claim, as 'fair use' is a defense to a copyright or trademark infringement claim and not a basis for an affirmative claim.\\n\\nAttorney 2: I agree. It's a clear example of a copyright infringement case not resulting in liability. Now that we have a case for each scenario, we can start preparing the final report.\\n\\nAttorney 3: Yes, we should also make sure to include a brief summary of the case, focusing on the main arguments, the court's reasoning, and the final verdict, as well as the source.\",      \n    \"Action\": \"Finish[In the case of BMG Music v. John Doe, the defendant was found liable for copyright infringement. The jury awarded BMG Music $675,000 in damages, which was later reduced to $67,500 by the judge (source: www.knowledgebase.beehive.systems/law-policy-and-ethics/dmca/notable-cases/bmg-music-v.-john-doe).\\n\\nOn the contrary, in a case involving Google, the defendant was not found liable for copyright infringement. A Pro se plaintiff sued Google over alleged censorship of social media posts and the court held that violation of 'fair use laws' is not a viable claim, as 'fair use' is a defense to a copyright or trademark infringement claim and not a basis for an affirmative claim (source: www.ipat.law.uci.edu/recent-fair-use-cases/).]\"      \n}      \n```"}]


        class BingSearchTool(BaseTool):
            name = "Intermediate Answer"
            description = "useful for when you need to answer questions about current events"

            def _run(self, query: str) -> str:
                # subscription_key = "6637a6554ede48ba9e240d97c318f4ec"
                subscription_key = "13835b8353af4f31959388f1494c29eb"
                endpoint = "https://api.bing.microsoft.com/v7.0/search"
                
                # Define the market as en-US
                mkt = 'en-US'
                
                # Construct parameters and headers for the API request
                params = {'q': query, 'mkt': mkt}
                headers = {'Ocp-Apim-Subscription-Key': subscription_key}
                
                try:
                    # Make the API request
                    response = requests.get(endpoint, headers=headers, params=params)
                    response.raise_for_status()
                    
                    # Extract relevant information from the response JSON
                    search_results = response.json().get('webPages', {}).get('value', [])

                    # Create a formatted result string
                    result_string = ""
                    for index, result in enumerate(search_results, start=1):
                        if index < 6 :
                            # result_string += f"{index}. {result['name']}\n   {result['snippet']}\n\n"
                            result_string += f"{index}. Topic: {result['name']} \n  Content: {result['snippet']}\n URL: {result['url']}\n\n "

                        else:
                            break
                
                    # print(result_string)
                    return result_string
                
                except Exception as ex:
                    return f"An error occurred: {str(ex)}"
            
            def _arun(self, query: str)-> str:
                raise NotImplementedError("This tool does not support async")



        # Define a Pydantic data model for the JSON response
        class InitialResponseData(BaseModel):
            Iteration: int
            Plan: str
            Thought: str
            Action: str

        class ResponseData(BaseModel):
            Iteration: int
            Thought: str
            Action: str

        def validate_dict(data_dict):
            try:
                # Check if data_dict has exactly 5 keys
                if len(data_dict) == 4:
                    Initial_response_data = InitialResponseData(**data_dict)
                    return Initial_response_data, None
                else:
                    # Validate the data_dict using the ResponseData model
                    response_data = ResponseData(**data_dict)
                    return response_data, None
            except ValidationError as e:
                # Handle validation errors
                return None, e
            
        # action driver code
        def perform_action(input_string):
            # Check if the input string starts with 'Search'
            if input_string.startswith('Search' or 'search'):
                # Extract the data inside square brackets
                start_index = input_string.find('[')
                end_index = input_string.find(']')
                
                if start_index != -1 and end_index != -1:
                    extracted_data = input_string[start_index + 1:end_index]
                    # print(f"Performing search action for: {extracted_data}")
                    return json.dumps(BingSearchTool()._run(extracted_data)), False

                else:
                    # print("No data inside square brackets found for search action.")
                    return "No data inside square brackets found for search action.", False
            
            # Check if the input string starts with 'Finish'
            elif input_string.startswith('Finish' or 'finish'):
                input_string = input_string.strip()
                # Extract the action part of the string
                start_index = input_string.find('[')
                # end_index = input_string.find(']') 
                end_index = -1
                
                # if start_index != -1 and end_index != -1:
                if start_index != -1:
                    action = input_string[start_index + 1:end_index]
                    # print(f"Performing finish action: {action}")
                    return action, True
                else:
                    return "No action inside square brackets found for finish action.", False
            
            else:
                return "Unknown action.", False

        def self_ask_plan_execute(question):
            que = f"""```\n{json.dumps({"Iteration": 1, "Question": question})}\n```"""
            prompt = sys_message.copy()
            prompt.append({"role":"user","content":que})

            n_calls, n_badcalls = 0, 0
            for i in range(1,8):
                response, total_tokens = llm(prompt)
                print(response)
                if i < 7:
                    n_calls += 1
                    for j in range(3):
                        try:
                            validated_data, validation_error = validate_dict(json.loads(response.strip("```")))
                            break
                        except:
                            response, total_tokens = llm(prompt)
                            if j == 2:
                                validated_data, validation_error = validate_dict(json.loads(response.strip("```")))
                            continue
                    if i == 1:
                        # understanding = validated_data.Understanding
                        try:
                            plan = validated_data.Plan
                        except:
                            pass

                    if validated_data:
                        thought = validated_data.Thought
                        action = validated_data.Action
                    
                    else:
                        n_badcalls += 1
                        n_calls += 1
                        continue
                    
                    observ, done = perform_action(action)
                    print(observ)
                    # obs = obs.replace('\\n', '')
                    obs = f"""```\n{json.dumps({"Iteration": i,"Observation": observ})}\n```"""
                    # print(type(obs))

                    prompt.append({"role":"assistant","content":response})
                    prompt.append({"role":"user","content" : obs})

                    if done:
                        return {"Input": question, "Output": observ}
                    
                else:
                    # final response query
                    if prompt[-1]["role"] == 'user':
                        prompt.append({"role":"assistant","content":response})
                    final_query = {
                        "Iteration": i,
                        "Observation": "Iteration Limit Exceeded, Please Generate Action: Finish[generating Finish Response with available data] Response to exit.",
                    }
                    
                    final_query = f"""```\n{json.dumps(final_query)}\n```"""

                    prompt.append({"role":"user","content": final_query})

                    llm_response, tokens = llm(prompt)
                    strip_response = llm_response.strip("```")
                    # finish_response,error = validate_dict(json.loads(strip_response))
                    finish_response,error = json.loads(strip_response), "None"

                    if finish_response:
                        observ, done = perform_action(finish_response["Action"])
                        return {"Input": question, "Output": observ}
                    else:
                        return {"Input": question, "Output": error}

            if not done:
                return {"Input": question, "Output": "Agent Stopped Due to Iteration Limit Exceed Error"}

        # def self_ask_plan_execute(question):
        #     que = f"""```\n{json.dumps({"Iteration": 1, "Question": question})}\n```"""
        #     prompt = sys_message.copy()
        #     prompt.append({"role":"user","content":que})

        #     n_calls, n_badcalls = 0, 0
        #     for i in range(1,8):
        #         if i < 7:
        #             n_calls += 1

        #             response, total_tokens = llm(prompt)
        #             # print(f"total token usage: {total_tokens}")

        #             validated_data, validation_error = validate_dict(json.loads(response.strip("```")))

        #             if validated_data:
        #                 thought = validated_data.Thought
        #                 action = validated_data.Action
                    
        #             else:
        #                 print(f"Bad Call....\n{validation_error}")
        #                 n_badcalls += 1
        #                 n_calls += 1
        #                 continue
                    
        #             observ, done = perform_action(action)
        #             # obs = obs.replace('\\n', '')
        #             obs = f"""```\n{json.dumps({"Iteration": i,"Observation": observ})}\n```"""
        #             # print(type(obs))

        #             prompt.append({"role":"assistant","content":response})
        #             prompt.append({"role":"user","content" : obs})

        #             if done:
        #                 return {"Input": question, "Output": observ}
                    
        #         else:
        #             # final response query
        #             final_query = {
        #                 "Iteration": 7,
        #                 "Thought": "Iteration Limit Exceeded, generating Finish Response with available data.",
        #                 "Action": "Finish[GENERATE YOUR FINAL REPORT HERE USING GATHERED INFO]"
        #             }
                    
        #             final_query = f"""```\n{json.dumps(final_query)}\n```"""
        #             finish_response,error = validate_dict(llm(final_query).strip("```"))
        #             if finish_response:
        #                 observ, done = perform_action((finish_response.Action))
        #                 return {"Input": question, "Output": observ}
        #             else:
        #                 return {"Input": question, "Output": error}

        #     if not done:
        #         return {"Input": question, "Output": "Agent Stopped Due to Iteration Limit Exceed Error"}

        try:
            ans = self_ask_plan_execute(query)
            return func.HttpResponse(json.dumps(ans), status_code=200)
        
        except Exception as e:
            return func.HttpResponse(json.dumps({"Input":query,"Output": str(e) }), status_code=200)
        
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
