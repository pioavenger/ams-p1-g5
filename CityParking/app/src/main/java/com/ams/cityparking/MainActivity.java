package com.ams.cityparking;

import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import android.util.Log;
import android.content.Intent;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;
import java.net.URL;

import java.net.MalformedURLException;


public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.d("CityParking-MA", "kkk");
        // set url

        // read url preferences
        SharedPreferences sp = this.getSharedPreferences("url_prefs", this.MODE_PRIVATE);
        String url = sp.getString("url", "");

        // first time
        if (url.equals("")) {
            url = "127.0.0.1:8000";
        }

        // read login preferences
        sp = this.getSharedPreferences("login_prefs", this.MODE_PRIVATE);
        String email = sp.getString("email", "");

        if (email.equals("")){ // not logged in
            setContentView(R.layout.activity_main);
            // set hint
            Log.d("CityParking-MA", "1");
            TextView url_text_view = (TextView) findViewById(R.id.test_url_text);
            Log.d("CityParking-MA", "2");
            url_text_view.setHint(url);
            Log.d("CityParking-MA", "3");
        }else{ // logged in
            // redirect to home
            startActivity(new Intent(this, HomeActivity.class));
        }
    }

    public void start(View view) {
        Intent intent = new Intent(this, LoginActivity.class);
        startActivity(intent);
        finish();
    }

    public void save(View view) {
        // get url from text view
        TextView url_text_view = (TextView) findViewById(R.id.test_url_text);
        String url_text = url_text_view.getText().toString();
        Log.d("CityParking-MA",url_text);
        if(!url_text.equals("")) {
            SharedPreferences sp = this.getSharedPreferences("url_prefs", this.MODE_PRIVATE);
            SharedPreferences.Editor editor = sp.edit();
            // check url formatting
            try {
                // check format
                URL url = new URL("http://"+url_text);

                editor.putString("url", url_text);
                editor.commit();

                Toast toast = Toast.makeText(this, "saved config" ,Toast.LENGTH_SHORT);
                toast.show();

                url_text_view.setText("");
                url_text_view.setHint(url_text);
            }catch (MalformedURLException e) {
                Toast toast = Toast.makeText(this, "wrong format!" ,Toast.LENGTH_SHORT);
                toast.show();
            }
        }else{
            Toast toast = Toast.makeText(this, "empty field!" ,Toast.LENGTH_SHORT);
            toast.show();
        }
    }
}
