package com.iot.ethanwright.iotcontroller;
import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.ImageView;
import android.widget.Switch;
import android.widget.TextView;

import org.apache.commons.io.IOUtils;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.util.Random;


/**
 * Ethan Wright
 */

public class MainActivity extends Activity {
    public String api_call;
    public String[] adjectives =  {"dangerous","penitent","like","silly","military","difficult","equable","magical","lucky","exotic","fluffy","dashing","wonderful","future","axiomatic","outrageous","striped","dramatic","strong","spicy","faithful","splendid","tricky","delicate","jumpy","precious","decisive","teeny-tiny","talented","loud","astonishing","profuse","large","beneficial","various","regular","little","coherent","diligent","lively","unusual","fluttering","equal","spotted","luxuriant","adjoining","swift","bright","fast","gorgeous","tasteful","hushed","caring","square","bouncy","ambitious","dynamic","frail","fanatical","awesome","kind","cluttered","political","electric","cuddly","immense","reminiscent","fierce","enormous","thundering","selective","safe","learned","lazy","happy","long-term","towering","testy","silent","tranquil","grateful","elated","proud","aboriginal","powerful","high-pitched","waiting","violet","fabulous","plausible","supreme","different","youthful","momentous","decorous","fretful","distinct","purple","efficient","spiffy","nippy","aquatic"};
    public String[] nouns = {"lumber","house","orange","shake","branch","yak","furniture","flock","zinc","yam","home boy","judge","flame","bird","baseball","burst","rainstorm","history","rod","grain","lamp","flower","cake","cobweb","idea","stream","pie","smile","pencil","plane","bird","snail","celery","mouse","truck","ink","camera","foot","tooth","loaf","card","sheet","flag","basketball","voice","minister","door","stew","maid","jelly","drawer","picture","hill","passenger","plastic","scale","nest","sister","invention","direction","horse","soup","wall","cow","committee","fork","man","toothpaste","dirt","bucket","moon","floor","paper","spy","engine","animal","cream","laborer","wine","cub","riddle","oatmeal","creature","insect","cracker","tongue","vacation","cloth","metal","volleyball"};

    public void randomize(){
        TextView randText = (TextView) findViewById(R.id.random);
        Random rand = new Random();
        String adjective = adjectives[rand.nextInt(adjectives.length)];
        String noun = nouns[rand.nextInt(nouns.length)];
        String message = "Hello my " + adjective + " " + noun + "!";
        randText.setText(message);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Button lights_on = (Button)findViewById(R.id.hue_on);
        Button lights_off = (Button)findViewById(R.id.hue_off);
        Switch bedroom = (Switch) findViewById(R.id.bedroom_on);
        Switch living_room = (Switch) findViewById(R.id.living_on);

        bedroom.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if(isChecked){
                    new AsyncUploadTest().execute();
                    api_call = "{`hue` : { `group` : `bedroom`, `rgb` : `.8,.6,.1`, `brightness` : `100`, `on` : `True` }}".replace('`','"');
                }else{
                    api_call = "{`hue` : { `group` : `bedroom`, `rgb` : `.8,.6,.1`, `brightness` : `100`, `on` : `False` }}".replace('`','"');
                    new AsyncUploadTest().execute();
                }
                // do something, the isChecked will be
                // true if the switch is in the On position
            }
        });
        living_room.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if(isChecked){
                    api_call = "{`hue` : { `group` : `fan`, `rgb` : `.8,.6,.1`, `brightness` : `100`, `on` : `True` }}".replace('`','"');
                    new AsyncUploadTest().execute();
                }else{
                    api_call = "{`hue` : { `group` : `fan`, `rgb` : `.8,.6,.1`, `brightness` : `100`, `on` : `False` }}".replace('`','"');
                    new AsyncUploadTest().execute();
                }
                // do something, the isChecked will be
                // true if the switch is in the On position
            }
        });


        api_call = "{`check hue` : { `group` : `fan` } }".replace('`','"');
        new AsyncUploadTest().execute();

        randomize();


        lights_on.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                api_call = "{`hue` : { `group` : `all`, `rgb` : `.8,.6,.1`, `brightness` : `100`, `on` : `True` }}".replace('`','"');
                new AsyncUploadTest().execute();
            }
        });
         lights_off.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                api_call = "{`hue` : { `group` : `all`, `rgb` : `.8,.6,.1`, `brightness` : `100`, `on` : `False` }}".replace('`','"');
                new AsyncUploadTest().execute();
            }
        });
    }

    private class AsyncUploadTest extends AsyncTask<Void,Void,Boolean>
    {
        private void setText(JSONObject mainObject) throws JSONException {
            final ImageView light_icon = (ImageView)  findViewById(R.id.light_icon);
            final Button lights_on = (Button) findViewById(R.id.hue_on);
            final Button lights_off = (Button) findViewById(R.id.hue_off);
            final Switch bed_status = (Switch)  findViewById(R.id.bedroom_on);
            final Switch living_status = (Switch)  findViewById(R.id.living_on);
            JSONObject hue = mainObject.getJSONObject("hue result");
            JSONObject fan = hue.getJSONObject("fan");
            JSONObject bedroom = hue.getJSONObject("bedroom");
            JSONObject bed_state = bedroom.getJSONObject("state");
            JSONObject state = fan.getJSONObject("state");
            final Boolean fan_all_on = state.getBoolean("all_on");
            final Boolean bed_all_on = bed_state.getBoolean("all_on");
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    if(bed_all_on){
                        bed_status.setChecked(true);
                    }
                    if(bed_all_on == false){
                        bed_status.setChecked(false);
                    }

                    if(fan_all_on){
                        living_status.setChecked(true);
                        light_icon.setImageResource(R.drawable.ic_moon_on);
                        lights_off.setElevation(12);
                        lights_on.setElevation(6);

                    }
                    if(fan_all_on == false){
                        living_status.setChecked(false);
                        light_icon.setImageResource(R.drawable.ic_moon_off);
                        lights_on.setElevation(12);
                        lights_off.setElevation(6);
                    }

                }
            });

        }
        @Override
        protected Boolean doInBackground(Void... v) {
            try {
                URL url = new URL("http://73.78.132.90:5000/");

                HttpURLConnection connection = (HttpURLConnection)url.openConnection();
                Log.d("Test","url: "+connection.getURL());

                connection.setUseCaches(false);
                connection.setDoOutput(true);
                connection.setDoInput(true);

                connection.setRequestMethod("POST");
                connection.setRequestProperty("Connection", "Keep-Alive");
                connection.setRequestProperty("Cache-Control", "no-cache");
                connection.setRequestProperty("Content-Type","application/json;charset=utf-8");
                connection.setRequestProperty("Accept","application/json");

                OutputStreamWriter writer = new OutputStreamWriter(connection.getOutputStream());
                writer.write(api_call);
                writer.flush();
                writer.close();

                Log.d("Test","json sent");

                int httpResult = connection.getResponseCode();
                Log.d("Test","http response code: "+httpResult);
                if(httpResult == HttpURLConnection.HTTP_OK)
                {
                    String text = IOUtils.toString(connection.getInputStream());
                    JSONObject mainObject = new JSONObject(text);
                    setText(mainObject);
                    Log.d("Test", IOUtils.toString(connection.getInputStream()));
                    Log.d("Test", "result read");
                }

            } catch (MalformedURLException e) {
                Log.e("Test","exception while sending data to server",e);
            } catch (ProtocolException e) {
                Log.e("Test","exception while sending data to server",e);
            } catch (IOException e) {
                Log.e("Test","exception while sending data to server",e);
            } catch (JSONException e) {
                e.printStackTrace();
            }
            return null;
        }
    }
}
