from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# 여기에 본인의 OpenAI API 키를 넣으세요
openai.api_key = "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"

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        user_input = request.form["resume_text"]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "너는 취업 자소서를 첨삭해주는 전문가야. 첨삭할 때는 단순히 고치지 말고, 피드백 형식으로 말해줘. 예: '이 문장은 너무 추상적이니 구체적인 행동으로 바꾸세요'."},
                    {"role": "user", "content": f"다음 자소서를 코멘트 형식으로 첨삭해줘, 실제로 대화하듯이 얘기해줘, 문장구조나 가독성면에서 개선해야 할 부분이 있으면 마지막 말로 얘기해줘, 숫자는 붙이지 말고 얘기해줘, 피드백 준 부분을 어떻게 하면 더 좋게 개선할 수 있을지 구체적으로 예시를 들어주면서 피드백해줘줘:\n\n{user_input}"}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            feedback = response["choices"][0]["message"]["content"]

            # 피드백 전체를 하나의 div에 넣음
            formatted_feedback = f"<div class='feedback'><p>{feedback.replace('\n', '<br>')}</p></div>"
            result = formatted_feedback

        except openai.error.RateLimitError:
            result = "요청이 너무 많습니다. 잠시 후 다시 시도해 주세요."
        except openai.error.InvalidRequestError as e:
            result = f"잘못된 요청이 발생했습니다: {str(e)}"
        except Exception as e:
            result = f"오류가 발생했습니다: {str(e)}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)