QuestionCollection Contract

Field / relationship            Valid                           Invalid
---------------------------------------------------------------------------
prerequisite                    references existing question
    references non-existent question
cycle prerequisite              no cycles in prerequisites      cycles present in prerequisite chain
