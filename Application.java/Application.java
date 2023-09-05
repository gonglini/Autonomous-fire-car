import com.google.appinventor.components.runtime.HandlesEventDispatching;
import com.google.appinventor.components.runtime.EventDispatcher;
import com.google.appinventor.components.runtime.Form;
import com.google.appinventor.components.runtime.Component;
import com.google.appinventor.components.runtime.Label;
import com.google.appinventor.components.runtime.Image;
import com.google.appinventor.components.runtime.Button;
import com.google.appinventor.components.runtime.Web;
import com.google.appinventor.components.runtime.Sound;
import com.google.appinventor.components.runtime.Clock;
import com.google.appinventor.components.runtime.Notifier;
import com.google.appinventor.components.runtime.TextToSpeech;

class Screen1 extends Form implements HandlesEventDispatching {
  private Label TEAM_NAME;
  private Label APP_NAME;
  private Label IP;
  private Label 연결해제상태;
  private Image Image1;
  private Label STATUS;
  private Label Label3;
  private Button Button1;
  private Web Web1;
  private Sound Sound1;
  private Clock Clock1;
  private Notifier Notifier1;
  private TextToSpeech TextToSpeech1;
  protected void $define() {
    this.AppName("firefire");
    this.Title("Screen1");
    TEAM_NAME = new Label(this);
    TEAM_NAME.Text("Text for Label1");
    APP_NAME = new Label(this);
    APP_NAME.Text("Text for Label2");
    IP = new Label(this);
    IP.Text("Text for Label3");
    연결해제상태 = new Label(this);
    연결해제상태.Text("Text for Label4");
    Image1 = new Image(this);
    Image1.Picture("Puple.png");
    STATUS = new Label(this);
    STATUS.Text("Text for Label5");
    Label3 = new Label(this);
    Label3.Text("Text for Label6");
    Button1 = new Button(this);
    Button1.Text("Text for Button1");
    Web1 = new Web(this);
    Sound1 = new Sound(this);
    Clock1 = new Clock(this);
    Notifier1 = new Notifier(this);
    TextToSpeech1 = new TextToSpeech(this);
    EventDispatcher.registerEventForDelegation(this, "InitializeEvent", "Initialize" );
    EventDispatcher.registerEventForDelegation(this, "TimerEvent", "Timer" );
    EventDispatcher.registerEventForDelegation(this, "GotTextEvent", "GotText" );
  }
  public boolean dispatchEvent(Component component, String componentName, String eventName, Object[] params){
    if( component.equals(this) && eventName.equals("Initialize") ){
      thisInitialize();
      return true;
    }
    if( component.equals(Clock1) && eventName.equals("Timer") ){
      Clock1Timer();
      return true;
    }
    if( component.equals(Web1) && eventName.equals("GotText") ){
      Web1GotText((String)params[0], (Integer)params[1], (String)params[2], (String)params[3]);
      return true;
    }
    return false;
  }
  public void thisInitialize(){
    if(연결해제상태.Text().equals("연결 해제 상태 입니다.")){
      if(연결해제상태.Text().equals("연결 상태 입니다.")){
        STATUS.Text("");
        STATUS.FontSize(Float.valueOf(22));
      }
    }
    STATUS.Text("연결 해제 상태");
    STATUS.FontSize(Float.valueOf(20));
  }
  public void Clock1Timer(){
    Web1.Url("http://172.20.10.10");
  }
  public void Web1GotText(String url, int responseCode, String responseType, String responseContent){
    IP.Text(Web1.Url());
    STATUS.Text("");
    STATUS.Text(responseContent);
    연결해제상태.Text("연결 상태 입니다.");
    if(STATUS.Text().equals("화재 감지 중")){
      Image1.Picture("Puple.png");
    }
   if (STATUS.Text().equals("화재 발생!!")) {
    Sound1.Play();
    createFireNotification("화재 발생!!", "비전타워 B2층 화재 발생");
    Image1.Picture("Image2.png");
    STATUS.BackgroundColor(Component.COLOR_NONE);
} else if (STATUS.Text().equals("화재 진압 중")) {
    Sound1.Play();
    createFireNotification("화재 진압 중!!", "로봇이 화재를 진압 중입니다.");
    Image1.Picture("Image3.png");
    STATUS.BackgroundColor(Component.COLOR_NONE);
} else if (STATUS.Text().equals("화재 진압 완료")) {
    Sound1.Stop();
    createFireNotification("화재 진압 완료", "화재 장소를 확인하세요.");
    Image1.Picture("Image3.png");
    STATUS.BackgroundColor(Component.COLOR_NONE);
} else if (STATUS.Text().equals("연결 해제 상태")) {
    createUnstableConnectionNotification("연결이 불안정합니다.", "재접속을 권장합니다.");
}

 private void createFireAlertNotification(String message, boolean isFireAlert) {
    String title = "화재 알림";
    int notificationId = 3;

    // 알림 콘텐츠 설정
    Notification.Builder builder = new Notification.Builder(this);
    builder.setContentTitle(title);
    builder.setContentText(message);
    builder.setSmallIcon(android.R.drawable.ic_dialog_alert);
    builder.setPriority(Notification.PRIORITY_HIGH);
    builder.setAutoCancel(true);

   
    if (isFireAlert) {
        builder.setSound(android.provider.Settings.System.DEFAULT_NOTIFICATION_URI);
    }

   
    NotificationManager notificationManager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
    notificationManager.notify(notificationId, builder.build());
}

Button1.setOnClickListener(new View.OnClickListener() {
    @Override
    public void onClick(View v) {
        String title = "비전 타워 B2층";
        String message = "화재 발생";
        NotificationManager notificationManager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
        NotificationCompat.Builder builder = new NotificationCompat.Builder(getApplicationContext())
                .setSmallIcon(android.R.drawable.ic_dialog_alert)
                .setContentTitle(title)
                .setContentText(message)
                .setPriority(NotificationCompat.PRIORITY_HIGH)
                .setAutoCancel(true);
        notificationManager.notify(0, builder.build());
    }
});