Name                                                   Stmts   Miss  Cover
--------------------------------------------------------------------------
chatbotAI/__init__.py                                      0      0   100%
chatbotAI/asgi.py                                          4      4     0%
chatbotAI/settings.py                                     28      1    96%
chatbotAI/urls.py                                          5      0   100%
chatbotAI/wsgi.py                                          4      4     0%
manage.py                                                 11     11     0%
users/__init__.py                                          0      0   100%
users/admin.py                                             3      0   100%
users/apps.py                                              4      0   100%
users/forms.py                                            28      1    96%
users/migrations/0001_initial.py                           7      0   100%
users/migrations/0002_alter_businessuserdata_user.py       6      0   100%
users/migrations/__init__.py                               0      0   100%
users/mixins.py                                           14      0   100%
users/models.py                                            8      0   100%
users/templatetags/__init__.py                             0      0   100%
users/templatetags/form_tags.py                            5      0   100%
users/tests.py                                             1      1     0%
users/tests/__init__.py                                    0      0   100%
users/tests/test_forms.py                                 25      0   100%
users/tests/test_mixins.py                                33      2    94%
users/tests/test_models.py                                21      0   100%
users/tests/test_project_optional_tests.py                19      6    68%
users/tests/test_project_urls.py                          11      2    82%
users/tests/test_template_tags.py                         16      0   100%
users/tests/test_urls.py                                  15      0   100%
users/tests/test_views.py                                129      0   100%
users/urls.py                                              9      2    78%
users/views.py                                           100     14    86%
--------------------------------------------------------------------------
TOTAL                                                    506     48    91%



# second run after full code refactor and finish all apps
Name                                                 Stmts   Miss  Cover
------------------------------------------------------------------------
agents/__init__.py                                       0      0   100%
agents/admin.py                                          3      0   100%
agents/app_utils/__init__.py                             0      0   100%
agents/app_utils/ai_personality.py                      32     17    47%
agents/app_utils/beautiful_graph_output.py              17      3    82%
agents/app_utils/call_llm.py                            41     14    66%
agents/app_utils/delete_embeddings.py                   11      0   100%
agents/app_utils/embed_data.py                          37      0   100%
agents/app_utils/formatters.py                          20      1    95%
agents/app_utils/json_dumps_manager.py                   8      0   100%
agents/app_utils/prompt_creation.py                     10      0   100%
agents/app_utils/retrieve_answer.py                    114     38    67%
agents/app_utils/token_count_helper.py                  11      0   100%
agents/apps.py                                           4      0   100%
agents/graph/__init__.py                                 0      0   100%
agents/graph/retrieval_agent_graph.py                  223    175    22%
agents/llms/__init__.py                                  0      0   100%
agents/llms/llms.py                                     11      0   100%
agents/models.py                                         4      0   100%
agents/prompts/__init__.py                               0      0   100%
agents/prompts/prompts.py                                9      0   100%
agents/structured_output/__init__.py                     0      0   100%
agents/structured_output/structured_output.py            6      0   100%
agents/tools/__init__.py                                 0      0   100%
agents/tools/tools.py                                   56      5    91%
agents/urls.py                                           4      0   100%
agents/views.py                                        133     28    79%
businessdata/__init__.py                                 0      0   100%
businessdata/admin.py                                    3      0   100%
businessdata/apps.py                                     4      0   100%
businessdata/forms.py                                   14      0   100%
businessdata/mixins.py                                  14      0   100%
businessdata/models.py                                  15      0   100%
businessdata/urls.py                                     4      0   100%
businessdata/views.py                                  172     67    61%
chatbotAI/__init__.py                                    0      0   100%
chatbotAI/asgi.py                                        4      4     0%
chatbotAI/settings.py                                   30      0   100%
chatbotAI/urls.py                                        5      0   100%
chatbotAI/wsgi.py                                        4      4     0%
chatbotsettings/__init__.py                              0      0   100%
chatbotsettings/admin.py                                 3      0   100%
chatbotsettings/apps.py                                  4      0   100%
chatbotsettings/forms.py                                13      0   100%
chatbotsettings/models.py                               32     11    66%
chatbotsettings/urls.py                                  4      0   100%
chatbotsettings/views.py                               103     73    29%
clientchat/__init__.py                                   0      0   100%
clientchat/admin.py                                      3      0   100%
clientchat/apps.py                                       4      0   100%
clientchat/forms.py                                     10      0   100%
clientchat/models.py                                    11      0   100%
clientchat/urls.py                                       4      0   100%
clientchat/views.py                                    159     37    77%
common/__init__.py                                       0      0   100%
common/admin.py                                          3      0   100%
common/apps.py                                           4      0   100%
common/discord_notifications.py                         70     56    20%
common/logs_filters.py                                   7      0   100%
common/middleware_logs_custom.py                        14      0   100%
common/models.py                                         8      0   100%
common/record_to_db.py                                  32      1    97%
common/templatetags/__init__.py                          0      0   100%
common/templatetags/form_tags.py                        11      0   100%
common/urls.py                                           4      0   100%
common/views.py                                         57      0   100%
log_analysis_center/__init__.py                          0      0   100%
log_analysis_center/beautiful_graph_output.py           17     17     0%
log_analysis_center/call_llm.py                         26     26     0%
log_analysis_center/chunk_store_analyze_logs.py         72     72     0%
log_analysis_center/delete_log_analyzer_data.py         34     34     0%
log_analysis_center/discord_notifications.py            87     87     0%
log_analysis_center/formatters.py                       15     15     0%
log_analysis_center/json_dumps_manager.py                8      8     0%
log_analysis_center/llms.py                             11     11     0%
log_analysis_center/log_analyzer_graph.py              216    216     0%
log_analysis_center/log_copier.py                       33     33     0%
log_analysis_center/logs_advice_report_creation.py      78     78     0%
log_analysis_center/prompt_creation.py                  10     10     0%
log_analysis_center/prompts.py                           2      2     0%
log_analysis_center/structured_output.py                 1      1     0%
log_analysis_center/token_count_helper.py                5      5     0%
log_analysis_center/tools.py                            26     26     0%
users/__init__.py                                        0      0   100%
users/admin.py                                           3      0   100%
users/apps.py                                            4      0   100%
users/forms.py                                          62      1    98%
users/models.py                                         10      0   100%
users/serializers.py                                    10     10     0%
users/urls.py                                            4      0   100%
users/views.py                                         155     40    74%
------------------------------------------------------------------------
TOTAL                                                 2472   1226    50%


# third run after full coverage done even the ones that i had forgotten in the second run
- This time we asked for markdown format and also we omitted the files that are agents so too complicated to cover test and other ones thta we want to keep in codebase but are nto used like the django rest-framework ones formt he beginning of the project
  we just want to keep trace of those as experience of done before.
```bash
# command or put the `--omit` file path in `.coveragerc` file: 
coverage report --format=markdown --omit=log_analysis_center/*,users/serializers.py,chatbotAI/asgi.py,chatbotAI/wsgi.py,agents/graph/*
```
| Name                                            |    Stmts |     Miss |   Cover |
|------------------------------------------------ | -------: | -------: | ------: |
| agents/admin.py                                 |        3 |        0 |    100% |
| agents/app\_utils/ai\_personality.py            |       32 |       17 |     47% |
| agents/app\_utils/beautiful\_graph\_output.py   |       17 |        3 |     82% |
| agents/app\_utils/call\_llm.py                  |       41 |       14 |     66% |
| agents/app\_utils/delete\_embeddings.py         |       11 |        0 |    100% |
| agents/app\_utils/embed\_data.py                |       37 |        0 |    100% |
| agents/app\_utils/formatters.py                 |       20 |        1 |     95% |
| agents/app\_utils/json\_dumps\_manager.py       |        8 |        0 |    100% |
| agents/app\_utils/prompt\_creation.py           |       10 |        0 |    100% |
| agents/app\_utils/retrieve\_answer.py           |      114 |       38 |     67% |
| agents/app\_utils/token\_count\_helper.py       |       11 |        0 |    100% |
| agents/apps.py                                  |        4 |        0 |    100% |
| agents/llms/llms.py                             |       11 |        0 |    100% |
| agents/models.py                                |        4 |        0 |    100% |
| agents/prompts/prompts.py                       |        9 |        0 |    100% |
| agents/structured\_output/structured\_output.py |        6 |        0 |    100% |
| agents/tools/tools.py                           |       56 |        5 |     91% |
| agents/urls.py                                  |        4 |        0 |    100% |
| agents/views.py                                 |      133 |       28 |     79% |
| businessdata/admin.py                           |        3 |        0 |    100% |
| businessdata/apps.py                            |        4 |        0 |    100% |
| businessdata/forms.py                           |       14 |        0 |    100% |
| businessdata/mixins.py                          |       14 |        0 |    100% |
| businessdata/models.py                          |       15 |        0 |    100% |
| businessdata/urls.py                            |        4 |        0 |    100% |
| businessdata/views.py                           |      172 |       67 |     61% |
| chatbotAI/settings.py                           |       30 |        0 |    100% |
| chatbotAI/urls.py                               |        5 |        0 |    100% |
| chatbotsettings/admin.py                        |        3 |        0 |    100% |
| chatbotsettings/apps.py                         |        4 |        0 |    100% |
| chatbotsettings/forms.py                        |       13 |        0 |    100% |
| chatbotsettings/models.py                       |       34 |       11 |     68% |
| chatbotsettings/urls.py                         |        4 |        0 |    100% |
| chatbotsettings/views.py                        |      103 |       73 |     29% |
| clientchat/admin.py                             |        3 |        0 |    100% |
| clientchat/apps.py                              |        4 |        0 |    100% |
| clientchat/forms.py                             |       10 |        0 |    100% |
| clientchat/models.py                            |       11 |        0 |    100% |
| clientchat/urls.py                              |        4 |        0 |    100% |
| clientchat/views.py                             |      159 |       37 |     77% |
| common/admin.py                                 |        3 |        0 |    100% |
| common/apps.py                                  |        4 |        0 |    100% |
| common/discord\_notifications.py                |       70 |       56 |     20% |
| common/logs\_filters.py                         |        7 |        0 |    100% |
| common/middleware\_logs\_custom.py              |       14 |        0 |    100% |
| common/models.py                                |        8 |        0 |    100% |
| common/record\_to\_db.py                        |       32 |        1 |     97% |
| common/templatetags/form\_tags.py               |       11 |        0 |    100% |
| common/urls.py                                  |        4 |        0 |    100% |
| common/views.py                                 |       57 |        0 |    100% |
| users/admin.py                                  |        3 |        0 |    100% |
| users/apps.py                                   |        4 |        0 |    100% |
| users/forms.py                                  |       62 |        1 |     98% |
| users/models.py                                 |       10 |        0 |    100% |
| users/urls.py                                   |        4 |        0 |    100% |
| users/views.py                                  |      155 |       40 |     74% |
|                                       **TOTAL** | **1592** |  **392** | **75%** |
