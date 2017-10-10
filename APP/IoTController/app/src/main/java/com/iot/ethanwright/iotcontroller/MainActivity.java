package com.iot.ethanwright.iotcontroller;
import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import org.apache.commons.io.IOUtils;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;

/**
 * Ethan Wright
 */

public class MainActivity extends Activity {
    public String api_call;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Button lights_on = (Button)findViewById(R.id.hue_on);
        Button lights_off = (Button)findViewById(R.id.hue_off);
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
                    Log.d("Test", IOUtils.toString(connection.getInputStream()));
                    Log.d("Test", "result read");
                }

            } catch (MalformedURLException e) {
                Log.e("Test","exception while sending data to server",e);
            } catch (ProtocolException e) {
                Log.e("Test","exception while sending data to server",e);
            } catch (IOException e) {
                Log.e("Test","exception while sending data to server",e);
            }
            return true;
        }
    }
}
