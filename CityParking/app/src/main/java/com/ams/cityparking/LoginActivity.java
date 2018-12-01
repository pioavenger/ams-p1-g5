package com.ams.cityparking;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;

import android.util.Log;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

public class LoginActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
    }

    @Override
    public void onBackPressed() {
        Intent intent = new Intent(this, MainActivity.class);
        startActivity(intent);
        finish();
    }

    public void login(View view) {
        LoginNetWorkTask task = new LoginNetWorkTask("/signin",this);
        Log.d("CityParking","hmm");
        // get params
        String email = ((TextView) findViewById(R.id.user_text)).getText().toString();
        String password = ((TextView) findViewById(R.id.password_text)).getText().toString();
        // check params
        Toast toast;
        if(email.equals("") && password.equals("")){
            toast = Toast.makeText(this, "insert email and password" ,Toast.LENGTH_SHORT);
            toast.show();
        }else if(email.equals("")){
            toast = Toast.makeText(this, "insert email" ,Toast.LENGTH_SHORT);
            toast.show();
        }else if(password.equals("")){
            toast = Toast.makeText(this, "insert password" ,Toast.LENGTH_SHORT);
            toast.show();
        }else {
            String[] params = {"email=" + email, "password=" + password};
            // send
            task.execute(params);
        }
    }

    public void register(View view) {
        Intent intent = new Intent(this, SignupActivity.class);
        startActivity(intent);
    }
}
