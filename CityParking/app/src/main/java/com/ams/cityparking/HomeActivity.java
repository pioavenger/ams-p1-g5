package com.ams.cityparking;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.widget.TextView;

public class HomeActivity extends AppCompatActivity {

    private BottomNavigationView.OnNavigationItemSelectedListener mOnNavigationItemSelectedListener
            = new BottomNavigationView.OnNavigationItemSelectedListener() {

        @Override
        public boolean onNavigationItemSelected(@NonNull MenuItem item) {
            switch (item.getItemId()) {
                case R.id.navigation_home:
                    return true;
                case R.id.navigation_dashboard:
                    return true;
                case R.id.navigation_notifications:
                    return true;
            }
            return false;
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);
        BottomNavigationView navigation = (BottomNavigationView) findViewById(R.id.navigation);
        navigation.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener);

        // read login preferences
        SharedPreferences sp = this.getSharedPreferences("login_prefs", this.MODE_PRIVATE);
        String username = sp.getString("username", "");
        // change textview
        ((TextView) findViewById(R.id.username_welcome_text)).append(username);
    }

    public void logout(View view) {
        // get email
        SharedPreferences sp = this.getSharedPreferences("login_prefs", this.MODE_PRIVATE);
        String email = sp.getString("email", "");

        LogoutNetWorkTask task = new LogoutNetWorkTask("/signout",this);
        String[] params = {"email=" + email};
        Log.d("CityParking-HA",email);
        // send
        task.execute(params);
    }
}
