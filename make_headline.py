import markovify
import csv

# Get raw text as string.
with open("headlines.csv") as f:
    text = f.read()

# Build the model.
text_model = markovify.NewlineText(text, state_size=3)

# Print three randomly-generated sentences of no more than 140 characters
# for i in range(3):
#     print(text_model.make_short_sentence(280))

return text_model.make_short_sentence(280)
