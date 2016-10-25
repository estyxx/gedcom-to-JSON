module.exports = function(mongoose, PersonModel) {

	ObjectId = mongoose.Schema.ObjectId;

	var ParentalRelModel = mongoose.model("ParentalRelationship",{
		child_id: {type: ObjectId, ref: PersonModel},
		parent_id: {type: ObjectId, ref: PersonModel},
		relationshipType: String,
		subType: String,
		startDate: Date,
		endDate: Date
	});

	return ParentalRelModel;
};