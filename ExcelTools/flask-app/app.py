from flask import Flask, render_template, request
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)


def generate_histogram(data, interval):
    plt.hist(data, bins=interval, edgecolor='black')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram')

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image to base64 for HTML embedding
    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_histogram', methods=['POST'])
def generate():
    data = [float(x) for x in request.form.get('data').split(',')]
    interval = int(request.form.get('interval'))
    plot_url = generate_histogram(data, interval)
    return render_template('result.html', plot_url=plot_url)


if __name__ == '__main__':
    app.run(debug=True)
