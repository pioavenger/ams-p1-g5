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
    private String email;

    private BottomNavigationView.OnNavigationItemSelectedListener mOnNavigationItemSelectedListener
            = new BottomNavigationView.OnNavigationItemSelectedListener() {

        @Override
        public boolean onNavigationItemSelected(@NonNull MenuItem item) {
            switch (item.getItemId()) {
                case R.id.navigation_home:
                    Log.d("CityParking-HA","home");
                    return true;
                case R.id.navigation_dashboard:
                    Log.d("CityParking-HA","browse");
                    return true;
                case R.id.navigation_notifications:
                    Log.d("CityParking-HA","notification");
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
        email = sp.getString("email", "");
        // change textview
        ((TextView) findViewById(R.id.welcome_text)).append(" "+email.split("@")[0]);
    }

    public void logout(View view) {
        LogoutNetWorkTask task = new LogoutNetWorkTask("/signout",this);
        String[] params = {"email=" + email};
        Log.d("CityParking-HA",email);
        // send
        task.execute(params);
    }
}
