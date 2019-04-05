import {Component, ViewChild} from '@angular/core';
import { NavController, NavParams} from 'ionic-angular';
import { Events } from "ionic-angular";
import { RestProvider } from "../../providers/rest/rest";
import leaflet from 'leaflet';
import L from 'leaflet';
import '../../../node_modules/leaflet-routing-machine/dist/leaflet-routing-machine.js';


@Component({
  selector: 'page-map',
  templateUrl: 'map.html'
})
export class MapPage {

  @ViewChild('mapId') mapContainer;
  map: any;
  userDetails: any;
  venueMarker: any;
  venueRoute: any;
  user = {
    "username" :"",
    "first_name": "",
    "last_name": "",
    "lat": "",
    "long": ""
  }
  venueDetails: any;
  venue = {
    "name": "",
    "address": "",
    "long": "",
    "lat": "",
    "url": ""
  }


  constructor(public navCtrl: NavController, public navParams: NavParams,
              public events:Events, public restProvider: RestProvider) {

    // Get user details form the localstorage
    const storedUser = JSON.parse(localStorage.getItem('user'));
    this.userDetails = storedUser;
    this.user.first_name = this.userDetails.first_name;
    this.user.last_name = this.userDetails.last_name;
    this.user.username = this.userDetails.username;

    this.events.subscribe('venue:locate', (data) => {

      // Check to see if a body has been passed with the navigation from the search page
      // If it has extract the values and store them in the venue object.
      try {
        this.venueDetails = data;
        this.venue.name = this.venueDetails.name;
        this.venue.address = this.venueDetails.address;
        this.venue.long = this.venueDetails.longlat.longitude;
        this.venue.lat = this.venueDetails.longlat.latitude;
        this.venue.url = this.venueDetails.url

        if(this.venue.name != "") {
          this.addVenueToMap()
        }
      }
      catch (e) {
        console.log(e);
      }
    });
  }

  // Run this method when the page loads
  ionViewDidLoad() {
    // If the map is not made create the map
    if(this.mapContainer == undefined){
      this.LeafletMap();
    }

  }

  // User icon
  createUserIcon() {
    const myIcon = L.icon({
      iconUrl: '../../assets/icon/userIcon.png',
      iconSize: [35, 35],
      iconAnchor: [17, 35],
      popupAnchor: [0, -35],
      shadowSize: [68, 95],
      shadowAnchor: [22, 94]
    });
    return myIcon;
  }

  // Event icon
  createEventIcon() {
    const myIcon = L.icon({
      iconUrl: '../../assets/icon/musicIcon.png',
      iconSize: [35, 35],
      iconAnchor: [17, 35],
      popupAnchor: [0, -35],
      shadowSize: [68, 95],
      shadowAnchor: [22, 94]
    });
    return myIcon;
  }

  // Clear the map when navigating away from the page
  ionViewCanLeave(){
    document.getElementById("mainmap").outerHTML = "";
  }

  // Create the leaflet map and add the users location as a marker to it.
  LeafletMap() {
    this.map = leaflet.map('mapId').fitWorld();
    leaflet.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attributions: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
        '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © ' +
        '<a href="http://mapbox.com">Mapbox</a>',
      maxZoom: 18,
      minZoom: 1,
    }).addTo(this.map);
    this.map.locate({
      setView: true,
      maxZoom: 12,
      minZoom: 1
    }).on('locationfound', (e) => {
      let markerGroup = leaflet.featureGroup();
      this.user.lat = e.latitude;
      this.user.long = e.longitude;
      let marker: any = leaflet.marker([e.latitude, e.longitude], {icon: this.createUserIcon()}).on('click', () => {
        markerGroup.bindPopup("Hello " + this.user.first_name + ", this is your location!");
      });
      markerGroup.addLayer(marker);
      this.map.addLayer(markerGroup);
      }).on('locationerror', (err) => {
        alert(err.message);
    });
    
  }

  // Add the venues location to the map as a marker with the venue details in the popup
  addVenueToMap() {
    try {
      this.map.removeLayer(this.venueMarker);
    }
    catch (e) {
      console.log('This is the first venue')
    }
    try {
      let markerGroup = leaflet.featureGroup();
      this.venueMarker = leaflet.marker([this.venue.lat, this.venue.long], {icon: this.createEventIcon()}).on('click', () => {
        markerGroup.bindPopup('Venue: ' + '<a href="' + this.venue.url + '">' + this.venue.name + '</a><br>' +
         'Address: ' + this.venue.address);
      });
      markerGroup.addLayer(this.venueMarker);
      this.map.addLayer(markerGroup);
      this.addRouteToVenue();
    }
    catch (e) {
      console.log(e)
    }
  }

  // Routes the user to the venue
  addRouteToVenue() {
    try {
      this.map.removeControl(this.venueRoute);
    }
    catch (e) {
      console.log('This is the first route')
    }
    try {
      this.venueRoute = L.Routing.control({ waypoints: [
          leaflet.latLng(this.user.lat, this.user.long),
          leaflet.latLng(Number(this.venue.lat), Number(this.venue.long))
        ],
        maxZoom: 12,
        createMarker: false,
      });
      this.map.addControl(this.venueRoute);
    }
    catch (e) {
      console.log('routing not working')
    }
  }

}
