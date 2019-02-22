package main

import (
	"context"
	"log"
	"time"

	"github.com/mongodb/mongo-go-driver/bson"

	"github.com/mongodb/mongo-go-driver/x/bsonx"

	"github.com/mongodb/mongo-go-driver/mongo"
)

func getServerVersion(ctx context.Context, client *mongo.Client) (string, error) {
	serverStatus, err := client.Database("admin").RunCommand(
		ctx,
		bsonx.Doc{{"serverStatus", bsonx.Int32(1)}},
	).DecodeBytes()
	if err != nil {
		return "", err
	}

	version, err := serverStatus.LookupErr("version")
	if err != nil {
		return "", err
	}

	return version.StringValue(), nil
}

func main() {
	client, err := mongo.NewClient("mongodb://localhost:27017")
	if err != nil {
		panic(err)
	}
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	err = client.Connect(context.Background())
	if err != nil {
		panic(err)
	}
	defer client.Disconnect(ctx)
	db := client.Database("cian")
	cian := db.Collection("cian")
	res, err := cian.InsertOne(context.Background(), bson.M{"hello": "world"})
	if err != nil {
		panic(err)
	}
	id := res.InsertedID
	log.Println(id)
	ver, err := getServerVersion(ctx, client)
	if err != nil {
		panic(err)
	}
	log.Println(ver)
}
