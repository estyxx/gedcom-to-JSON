module.exports = function(mongoose, PersonModel) {

	ObjectId = mongoose.Schema.ObjectId;

	var PairBondModel = mongoose.model("PairBondRelationship",{
		personOne_id: {type: ObjectId, ref: PersonModel},
		personTwo_id: {type: ObjectId, ref: PersonModel},
		relationshipType: String,
		subType: String,
		startDate: Date,
		endDate: Date
	});

	return PairBondModel;
};