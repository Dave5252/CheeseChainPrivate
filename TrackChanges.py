import os.path

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport


def fetchChanges(ID):
    #change wd
    os.chdir(r"C:\Users\ddien\SOPRA\BA-Code\Answer")
    for item in os.listdir():
        open(item, "r")
        transport = AIOHTTPTransport(url="https://qs.fromarte.ch/graphql/",
                                     headers={"authorization": "Bearer " + self.getAuthToekn()})
        client = Client(transport=transport)
        # Provide a GraphQL query with th docID
        query = gql("""
                          query DocumentAnswers($id: ID!) {
          allDocuments(filter: [{id: $id}]) {
            edges {
              node {
                id
                form {
                  id
                  slug
                  __typename
                }
                workItem {
                  id
                  __typename
                }
                case {
                  id
                  workItems {
                    edges {
                      node {
                        id
                        task {
                          id
                          __typename
                        }
                        __typename
                      }
                      __typename
                    }
                    __typename
                  }
                  __typename
                }
                answers {
                  edges {
                    node {
                      ...FieldAnswer
                      __typename
                    }
                    __typename
                  }
                  __typename
                }
                __typename
              }
              __typename
            }
            __typename
          }
        }

        fragment SimpleQuestion on Question {
          id
          slug
          label
          isRequired
          isHidden
          meta
          infoText
          ... on TextQuestion {
            textMinLength: minLength
            textMaxLength: maxLength
            textDefaultAnswer: defaultAnswer {
              id
              value
              __typename
            }
            placeholder
            __typename
          }
          ... on TextareaQuestion {
            textareaMinLength: minLength
            textareaMaxLength: maxLength
            textareaDefaultAnswer: defaultAnswer {
              id
              value
              __typename
            }
            placeholder
            __typename
          }
          ... on IntegerQuestion {
            integerMinValue: minValue
            integerMaxValue: maxValue
            integerDefaultAnswer: defaultAnswer {
              id
              value
              __typename
            }
            placeholder
            __typename
          }
          ... on FloatQuestion {
            floatMinValue: minValue
            floatMaxValue: maxValue
            floatDefaultAnswer: defaultAnswer {
              id
              value
              __typename
            }
            placeholder
            __typename
          }
          ... on ChoiceQuestion {
            choiceOptions: options {
              edges {
                node {
                  id
                  slug
                  label
                  isArchived
                  __typename
                }
                __typename
              }
              __typename
            }
            choiceDefaultAnswer: defaultAnswer {
              id
              value
              __typename
            }
            __typename
          }
          ... on MultipleChoiceQuestion {
            multipleChoiceOptions: options {
              edges {
                node {
                  id
                  slug
                  label
                  isArchived
                  __typename
                }
                __typename
              }
              __typename
            }
            multipleChoiceDefaultAnswer: defaultAnswer {
              id
              value
              __typename
            }
            __typename
          }
          ... on DateQuestion {
            dateDefaultAnswer: defaultAnswer {
              id
              value
              __typename
            }
            __typename
          }
          ... on StaticQuestion {
            staticContent
            __typename
          }
          ... on CalculatedFloatQuestion {
            calcExpression
            __typename
          }
          ... on ActionButtonQuestion {
            action
            color
            validateOnEnter
            __typename
          }
          __typename
        }

        fragment FieldTableQuestion on Question {
          id
          ... on TableQuestion {
            rowForm {
              id
              slug
              questions {
                edges {
                  node {
                    ...SimpleQuestion
                    __typename
                  }
                  __typename
                }
                __typename
              }
              __typename
            }
            tableDefaultAnswer: defaultAnswer {
              id
              value {
                id
                answers {
                  edges {
                    node {
                      id
                      question {
                        id
                        slug
                        __typename
                      }
                      ... on StringAnswer {
                        stringValue: value
                        __typename
                      }
                      ... on IntegerAnswer {
                        integerValue: value
                        __typename
                      }
                      ... on FloatAnswer {
                        floatValue: value
                        __typename
                      }
                      ... on ListAnswer {
                        listValue: value
                        __typename
                      }
                      ... on DateAnswer {
                        dateValue: value
                        __typename
                      }
                      __typename
                    }
                    __typename
                  }
                  __typename
                }
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }

        fragment FieldQuestion on Question {
          id
          ...SimpleQuestion
          ...FieldTableQuestion
          ... on FormQuestion {
            subForm {
              id
              slug
              name
              questions {
                edges {
                  node {
                    id
                    ...SimpleQuestion
                    ...FieldTableQuestion
                    ... on FormQuestion {
                      subForm {
                        id
                        slug
                        name
                        questions {
                          edges {
                            node {
                              ...SimpleQuestion
                              ...FieldTableQuestion
                              __typename
                            }
                            __typename
                          }
                          __typename
                        }
                        __typename
                      }
                      __typename
                    }
                    __typename
                  }
                  __typename
                }
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }

        fragment SimpleAnswer on Answer {
          id
          question {
            id
            slug
            __typename
          }
          ... on StringAnswer {
            stringValue: value
            __typename
          }
          ... on IntegerAnswer {
            integerValue: value
            __typename
          }
          ... on FloatAnswer {
            floatValue: value
            __typename
          }
          ... on ListAnswer {
            listValue: value
            __typename
          }
          ... on FileAnswer {
            fileValue: value {
              id
              uploadUrl
              downloadUrl
              metadata
              name
              __typename
            }
            __typename
          }
          ... on DateAnswer {
            dateValue: value
            __typename
          }
          __typename
        }

        fragment FieldAnswer on Answer {
          id
          ...SimpleAnswer
          ... on TableAnswer {
            tableValue: value {
              id
              form {
                id
                slug
                questions {
                  edges {
                    node {
                      ...FieldQuestion
                      __typename
                    }
                    __typename
                  }
                  __typename
                }
                __typename
              }
              answers {
                edges {
                  node {
                    ...SimpleAnswer
                    __typename
                  }
                  __typename
                }
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }


                        """)
        response = client.execute(query, variable_values=params)
        return response


fetchChanges("ho")