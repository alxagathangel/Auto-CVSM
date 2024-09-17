import os
import matplotlib.pyplot as plt

def plotBar(df,file_name,output_dir):
    # Msg State
    plot_filename = os.path.join(output_dir,f'clean_{os.path.splitext(file_name)[0]}_plotBar.png')
    plt.figure(figsize=(8,5))
    msgs_counts = df.groupby('im_state')['msgs_count'].sum()
    #print("Messages: ",msgs_counts)
    colors = { 'seen':'blue' , 'delivered':'green' }
    msgs_counts.plot(kind='bar',stacked=True,color=[colors[im_state] for im_state in msgs_counts.index])
    plt.xlabel('IM State')
    plt.ylabel('Total Messages')
    plt.xticks(rotation=0)
    handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in colors]
    labels = [label for label in colors]
    plt.legend(handles, labels)
    plt.savefig(plot_filename)
    plt.close()

def plotArea(df,file_name,output_dir):
    # Daily Msgs
    plot_filename = os.path.join(output_dir,f'clean_{os.path.splitext(file_name)[0]}_plotArea.png')
    plt.figure(figsize=(15,6))
    daily_counts = df.groupby('full_date')['msgs_count'].sum()
    daily_counts.plot(kind='area',color='lightcoral',title='Daily Message Counts')
    plt.xlabel('Date')
    plt.ylabel('Total Messages')
    plt.grid(True)
    plt.savefig(plot_filename)
    plt.close()

def plotBox(df,file_name,output_dir):
    import seaborn as sns
    # Msgs by Day of Week
    plot_filename = os.path.join(output_dir,f'clean_{os.path.splitext(file_name)[0]}_plotBox.png')
    plt.figure(figsize=(12,6))
    df['day_of_week']=df['full_date'].dt.day_name()
    sns.boxplot(x='day_of_week',y='msgs_count',data=df,order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
    plt.title('Message Count Distribution by Day of Week')
    plt.xlabel('Day of Week')
    plt.ylabel('Total Messages')
    plt.savefig(plot_filename)
    plt.close()
