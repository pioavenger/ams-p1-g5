package com.ams.cityparking;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import com.ams.cityparking.NetWorkTools.SignupNetWorkTask;

public class SignupActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);
    }

    @Override
    public void onBackPressed() {
        Intent intent = new Intent(this, MainActivity.class);
        startActivity(intent);
        finish();
    }

    public void signin(View view) {
        Intent intent = new Intent(this, LoginActivity.class);
        startActivity(intent);
        finish();
    }

    public void signup(View view) {
        SignupNetWorkTask task = new SignupNetWorkTask("/signup",this);
        Log.d("CityParking","hmm");
        // get params
        String username = ((TextView) findViewById(R.id.user_text)).getText().toString();
        String password = ((TextView) findViewById(R.id.password_text)).getText().toString();
        String email = ((TextView) findViewById(R.id.email_text)).getText().toString();
        // check params
        Toast toast;
        if(email.equals("") || password.equals("") || username.equals("")){
            toast = Toast.makeText(this, "insert missing fields" ,Toast.LENGTH_SHORT);
            toast.show();
        }else {
            username = username.replace(" ","+");
            String[] params = {"mname="+username,"password1=" + password, "password2=" + password, "email=" + email, "carplate="+"AB-CD-EF"};
            // send
            task.execute(params);
        }
    }
}
