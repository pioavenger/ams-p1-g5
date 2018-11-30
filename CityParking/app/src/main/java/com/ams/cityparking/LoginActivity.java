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

    public void login(View view) {
        // change MainActivity.class to {ActivityName}.class
        LoginNetWorkTask task = new LoginNetWorkTask("http://192.168.1.76:8000/signin",this,new Intent(this, HomeActivity.class));
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
            toast = Toast.makeText(this, "insert email" ,Toast.LENGTH_SHORT);
            toast.show();
        }else {
            String[] params = {"email=" + email, "password=" + password};
            // send
            task.execute(params);
        }
    }

    public void goToStart(View view) {
        Intent intent = new Intent(this, MainActivity.class);
        startActivity(intent);
    }
}
