import matplotlib.pyplot as plt
import random
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from GetDiet import getdietchart
import requests
def GeneratePdfReport():
    # Url of database
    url = "https://ptrainer-567d7-default-rtdb.firebaseio.com/pt.json"

    # A GET request to the API to get number of reps
    response = requests.get(url)
    response_json = response.json()
    print(response_json)
    rep_data = []
    date_range = []
    for date in response_json:
        rep_data.append(response_json[date])
        date_range.append(date)
    colors = []
    for i in range(len(rep_data)):
        colors.append('#{:06x}'.format(random.randint(0, 256**3)))
    # create the bar graph with random colors
    fig, (ax1,wx2, ax2, ax3) = plt.subplots(nrows=4, figsize=(10, 15))
    ax1.bar(date_range[-14:-7], rep_data[-14:-7], width=0.5, color=colors)
    fig.subplots_adjust(hspace=0.5)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Number of Reps')
    ax1.set_title('Week 1 Performance')

    wx2.bar(date_range[-7:], rep_data[-7:], width=0.5, color=colors)
    wx2.set_xlabel('Date')
    wx2.set_ylabel('Number of Reps')
    wx2.set_title('Week 2 Performance')

    # calculate the weekly performance increase
    weekly_performance = []
    for i in range(1, len(rep_data[-14:])):
        weekly_increase = ((rep_data[i] - rep_data[i-1]) / rep_data[i-1]) * 100
        weekly_performance.append(weekly_increase)

    # create a pie chart to show performance insights
    labels = ['Avg. % Increase',"Avg Week 1 ","Avg Week 2"]
    week1,week2=sum(rep_data[-14:-7]) / 7,sum(rep_data[-7:])/7
    avg_increase =((week2-week1)/week1*100)
    best_increase = abs(max(weekly_performance))
    worst_increase =  min(weekly_performance)
    values = [abs(avg_increase),week1,week2]
    print(values)
    pie_colors = ['#00ff00',"#f87fff","#ff5733"]
    if avg_increase<0:
        labels[0]="Avg % Decrease"
        avg_increase=abs(avg_increase)
        pie_colors[0]='#ff0000'
    explode = (0.05,0.05,0.05)
    ax2.pie(np.array(values), labels=labels, colors=pie_colors, startangle=90, explode=explode, autopct= '%1.1f%%')
    ax2.axis('equal')

    ax2.set_title('Performance Insights')

    if best_increase >= 10:
        diet_plan = "Your performance is excellent! Keep up the good work and maintain your current diet."
    elif avg_increase >= 5:
        diet_plan = "Your performance is improving! Consider adding more lean protein and whole grains to your diet."
    elif worst_increase > 0:
        diet_plan = "Your performance is steady, but there is room for improvement. Try incorporating more fruits and vegetables into your diet."
    else:
        diet_plan = "Your performance is declining. Focus on eating a balanced diet with plenty of nutrients and hydration."

    ax3.text( -0.1,0.6,diet_plan+"\n"+"Best Increase ->"+str(best_increase)+"%\n"+"Worst Increase ->"+str(worst_increase)+"%\n"+"Max rep ->"+str(max(rep_data[-14:]))+" on "+date_range[rep_data.index(max(rep_data[-14:]))] +"\n"+"Min rep ->"+str(min(rep_data[-14:]))+" on "+date_range[rep_data.index(min(rep_data[-14:]))], fontsize=10)
    ax3.axis('off')
    with PdfPages('performance_report.pdf') as pdf:
        pdf.savefig(fig)
        fig,ax4=plt.subplots(figsize=(8, 15))
        diet_chart=getdietchart(avg_increase)
        ax4.set_title('Diet Chart for You')
        ax4.text(0, 0.5, diet_chart, fontsize=10,wrap=True)
        ax4.axis('off')
        pdf.savefig()

    plt.show()
