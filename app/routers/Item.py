class ImportItem(Base):
    __tablename__ = "import_items"

    id = Column(Integer, primary_key=True, index=True)
    receipt_id = Column(Integer, ForeignKey("import_receipts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    quantity = Column(Integer)
    price = Column(Float)
    total = Column(Float)

    receipt = relationship("ImportReceipt", back_populates="items")
    product = relationship("Product")
