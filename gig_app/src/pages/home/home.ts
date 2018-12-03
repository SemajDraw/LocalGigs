import { Component } from '@angular/core';
import { NavController} from 'ionic-angular';
import { LoginPage } from "../login/login";


@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {

  userDetails: any;
  user = {
    "first_name": "",
    "last_name": "",
    "username": "",
    "email": "",
    "age": "",
    "gender": "",
    "bio": ""
  }
  constructor(public navCtrl: NavController) {
    // Get the users details from localstorage and store them in the user object
    const storedUser = JSON.parse(localStorage.getItem('user'));
    this.userDetails = storedUser;

    this.user.first_name = this.userDetails.first_name;
    this.user.last_name = this.userDetails.last_name;
    this.user.username = this.userDetails.username;
    this.user.email = this.userDetails.email;
    this.user.age = this.userDetails.age;
    this.user.gender = this.userDetails.gender;
    this.user.bio = this.userDetails.bio;
  }

  // Clear local storage when the user logs out
  logOut() {
    // Clear the local storage and navigate to the login page
    localStorage.clear();
    this.navCtrl.push(LoginPage);
  }


}
