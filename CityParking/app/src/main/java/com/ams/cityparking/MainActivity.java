package com.ams.cityparking;

import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import android.content.Intent;
import android.view.View;


public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // read login preferences
        SharedPreferences sp = this.getSharedPreferences("login_prefs", this.MODE_PRIVATE);
        String email = sp.getString("email", "");
        String password = sp.getString("password", "");
        if(email.equals("") || password.equals(""))
            setContentView(R.layout.activity_main);
        else
            startActivity(new Intent(this, HomeActivity.class));
    }

    public void start(View view) {
        Intent intent = new Intent(this, LoginActivity.class);
        startActivity(intent);
    }
}
