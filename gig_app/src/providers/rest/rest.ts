import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

/*
  Generated class for the RestProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class RestProvider {

  baseUrl = 'http://52.209.96.131/localgigs/api/';
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
  userSignUp(username, firstName, lastName, email, password, passwordCon) {
    return new Promise(resolve => {
      this.http.post(this.baseUrl + 'rest_auth/registration', {
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
  searchGigs(gig, city) {
    const headers = this.createHeaders();
    return new Promise(resolve => {
      this.http.get(this.baseUrl + 'get_events/?search=' + gig + '&city=' + city, {headers: headers} )
        .subscribe(data => { resolve(data); }, err => { console.log(err);
        });
    });
  }

  // Make a GET request to the Django API which makes a GET request to the Ticketmaster API
  // which returns the details of the venue.
  venueInfo(venueId) {
    const headers = this.createHeaders();
    return new Promise(resolve => {
      this.http.get(this.baseUrl + 'get_venue_details/?venue_id=' + venueId, {headers: headers} )
        .subscribe(data => { resolve(data); }, err => { console.log(err);
        });
    });
  }

  // Create authorization headers for necessary requests
  createHeaders(){
    const token = this.getAuthToken();
     let headers = new HttpHeaders().set('Authorization', 'Token ' + token)

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
