package com.ams.cityparking;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;

import android.util.Log;
import android.view.View;

public class LoginActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
    }

    public void login(View view) {
        Log.d("login","start async task");
        // change MainActivity.class to {ActivityName}.class
        NetWorkTask task = new NetWorkTask(this,new Intent(this, MainActivity.class));
        task.execute("paramtest");
    }

    public void goToStart(View view) {
        Intent intent = new Intent(this, MainActivity.class);
        startActivity(intent);
    }
}
