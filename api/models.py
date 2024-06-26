from datetime import datetime
from typing import Dict, List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field
import uuid


class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    username: str
    password: str
    time: Optional[datetime]

    class Config:
        populate_by_name = True
        jscon_schema_extra = {
            "example": {
                "username": "john doe",
                "password": "hashed password",
                "time": datetime.now(),
            }
        }


class CreateUser(BaseModel):
    username: str
    password: str

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "username": "john doe",
                "password": "raw password",
            }
        }


class GetToken(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None


class GetPlaylist(BaseModel):
    playlist_id: str
    authorization_token: str


class Playlist(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    playlist_name: str
    user_id: uuid.uuid4
    time: Optional[datetime]
    tracks: List[str]

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "playlist_name": "test",
                "user_id": str(ObjectId()),
                "time": datetime.now(),
                "tracks": [str(ObjectId()), str(ObjectId())],
            }
        }


class PlaylistUpdate(BaseModel):
    playlist_name: Optional[str] = None
    tracks: Optional[List[str]] = None


class Track(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    track_name: str
    artist_name: str
    album_name: str
    analysis: Dict
    spotify: Dict
    time: Optional[datetime]

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "track_name": "test",
                "artist_name": "test",
                "album_name": "test",
                "analysis": {
                    "danceability": 0.393,
                    "energy": 0.588,
                    "key": 9,
                    "loudness": -6.68,
                    "mode": 0,
                    "speechiness": 0.0613,
                    "acousticness": 0.345,
                    "instrumentalness": 0,
                    "liveness": 0.134,
                    "valence": 0.728,
                    "tempo": 203.145,
                    "analysis_url": "https://api.spotify.com/v1/audio-analysis/1234",
                    "duration_ms": 186333,
                    "time_signature": 4,
                },
                "spotify": {
                    "track_id": "1234",
                    "uri": "spotify:track:1234",
                    "track_href": "https://api.spotify.com/v1/tracks/1234",
                },
                "time": datetime.now(),
            }
        }


class TrackUpdate(BaseModel):
    track_name: Optional[str] = None
    artist_name: Optional[str] = None
    album_name: Optional[str] = None
    analysis: Optional[Dict] = None
    spotify: Optional[Dict] = None


class PlaylistGenerate(BaseModel):
    keywords: str
    description: Optional[str] = None
    mood: str
    jwt: str

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "keywords": "list of keywords",
                "description": "detailed description of the playlist",
                "mood": "Happy",
                "jwt": str(ObjectId()),
            }
        }
