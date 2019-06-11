import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

/*
  Generated class for the RestProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class RestProvider {

  baseUrl = 'http://127.0.0.1:8000/api/';
  userDetails: any;


  constructor(public http: HttpClient) {

  }

  // Make GET request to the Django API to log user in and retrieve profile data and auth token
  userLogIn(email, password) {

    return new Promise((resolve, reject) => {
      this.http.get(this.baseUrl + 'login/?email=' + email + '&password=' + password)
        .subscribe(data => {
          resolve(data);
        },
            err => { reject(err); console.log(err);
        });
    });
  }

  // Make POST request the Django API to create a new user
  userSignUp(username, email, firstName, lastName, password, passwordCon) {
    return new Promise(resolve => {
      this.http.post(this.baseUrl + 'rest_auth/registration/', {
        "username": username,
        "email": email,
        "first_name": firstName,
        "last_name": lastName,
        "password1": password,
        "password2": passwordCon
    }).subscribe(data => { resolve(data); }, err => { console.log(err);});

    });
  }

  // Make a GET request to the Django API which makes a GET request to the Ticketmaster API
  // which returns a list of events.
  searchEvents(search) {
    const headers = this.createHeaders();
    return new Promise(resolve => {
      this.http.get(this.baseUrl + 'get_ticketmaster_events/?search='
        + search , {headers: headers} )
        .subscribe(data => { resolve(data); }, err => { console.log(err);
        });
    });
  }

  // Gets the users saved events from the database
  getSavedEvents () {
    const headers = this.createHeaders();
    return new Promise(resolve => {
    this.http.get(this.baseUrl + 'get_saved_events/', {headers: headers}
      ).subscribe(data => { resolve(data); }, err => { console.log(err);});
    });
  }

  // Gets the users recommended events from the database
  getRecommendedEvents () {
    const headers = this.createHeaders();
    return new Promise(resolve => {
    this.http.get(this.baseUrl + 'get_recommended_events/', {headers: headers}
      ).subscribe(data => { resolve(data); }, err => { console.log(err);});
    });
  }

  // Saves an event to the database
  saveEvent () {
    const headers = this.createHeaders();
    return new Promise(resolve => {
    this.http.get(this.baseUrl + 'save_event/', {headers: headers}
      ).subscribe(data => { resolve(data); }, err => { console.log(err);});
    });
  }

  // Gets the users interested list from db interested_gigs column
  deleteEvent () {
    const headers = this.createHeaders();
    return new Promise(resolve => {
    this.http.get(this.baseUrl + 'delete_event/', {headers: headers}
      ).subscribe(data => { resolve(data); }, err => { console.log(err);});
    });
  }

  // Create authorization headers for necessary requests
  createHeaders(){
    const token = this.getAuthToken();
     let headers = new HttpHeaders().set('Authorization', 'Token ' + token);

    return headers;
  }

  // Gets the users auth token from localstorage
  getAuthToken() {
    const storedUser = JSON.parse(localStorage.getItem('user'));
    this.userDetails = storedUser;
    const token = this.userDetails.token;

    return token;
  }
}
