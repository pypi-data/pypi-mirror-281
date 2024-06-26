from .models import *
from .dataset_loader import *

import os
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import torchvision.utils as vutils
import torch.nn as nn
import torch.optim as optim

def train(network, datasetloader, metadata_file, root_dir, epochs, batch_size, model):
    
    if network.lower() == "gan":
        train_gan(datasetloader, metadata_file, root_dir, epochs, batch_size, model)
    elif network.lower() == "cnn":
        train_cnn(datasetloader, metadata_file, root_dir, epochs, batch_size, model)
    else:
        print("Only gan and cnn are available for now.")


def train_cnn(datasetloader, metadata_file, root_dir, epochs, batch_size, model):
    
    # Define transforms
    transform = transforms.Compose([
        transforms.Resize((256, 256)),  # Resize images if necessary
        transforms.ToTensor(),          # Convert images to tensors
    ])

    # Create dataset and dataloader
    if datasetloader.lower() == "local":
        dataset = DatasetLoader(metadata_file=metadata_file, root_dir=root_dir, transform=transform) 
        print(f"Dataset length: {len(dataset)}")
    elif datasetloader.lower() == "internet":
        dataset = DatasetLoaderfromInternet(metadata_url=metadata_file, root_url=root_dir, transform=transform)
        print(f"Dataset length: {len(dataset)}")
    else:
        print(f"Can not find the specified dataset loader `{datasetloader}` from local and internet.\nPlease cheack properly.")
        SystemError
        SystemExit

    # Load one image to test
    try:
        sample_img = dataset[0]
        print(f"Sample image size: {sample_img.size()}")
    except FileNotFoundError as e:
        print(e)

    # Create DataLoader and Iterate
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Iterate over the DataLoader
    for i, batch in enumerate(dataloader):
        print(f"Batch {i+1}, Batch size: {batch.size()}")
        if i == 2:  # Only print first three batches
            break

    # Visualize Sample Images
    # Get a batch of training data
    for i, batch in enumerate(dataloader):
        if i == 0:  # Only visualize the first batch
            images = batch
            break

    # Make a grid from batch
    out = vutils.make_grid(images, padding=2, normalize=True)

    # Plot the grid
    plt.figure(figsize=(12, 12))
    plt.imshow(out.permute(1, 2, 0))
    plt.title('Batch of Images')
    #plt.show()

    # Check for GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Initialize the model
    if model.lower() == "usrcnn":
        model = USRCNN().to(device)
        print("Initialized the model")
    elif model.lower() == "esrcnn":
        model = ESRCNN().to(device)
        print("Initialized the model")
    elif model.lower() == "bsrcnn":
        model = BSRCNN().to(device)
        print("Initialized the model")
    elif model.lower() == "isrcnn":
        model = ISRCNN().to(device)
        print("Initialized the model")
    elif model.lower() == "rsrcnn":
        model = RSRCNN().to(device)
        print("Initialized the model")
    elif model.lower() == "srcnn":
        model = SRCNN().to(device)
        print("Initialized the model")
    else:
        print(f"Can not find the specified model `{model}` from usrcnn, esrcnn, bsrcnn, isrcnn, rsrcnn and srcnn.\nPlease cheack properly.")
        SystemError
        SystemExit

    # Define loss and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    print("Defined loss and optimizer")

    name = input("what would you like to call your model?: ")

    # Train the CNN
    print("Training Started")

    epochs=epochs

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        
        for batch_idx, inputs in enumerate(dataloader):
            inputs = inputs.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, inputs)  # Since it's an autoencoder, target is input
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

            # Print batch progress
            if batch_idx % 10 == 0:
                print(f'Epoch {epoch+1}/{epochs}, Batch {batch_idx}/{len(dataloader)}, Loss: {loss.item()}')
        
        # Print epoch progress
        print(f'Epoch {epoch+1}/{epochs}, Average Loss: {running_loss/len(dataloader)}')

    # Save the model
    model_name = name
    torch.save(model.state_dict(), f'{model_name}.pnn')
    print(f"Model saved at {os.path.abspath(model_name)}.pnn")


def train_gan(datasetloader, metadata_file, root_dir, epochs, batch_size, model):
    
    # Define transforms
    transform = transforms.Compose([
        transforms.Resize((256, 256)),  # Resize images if necessary
        transforms.ToTensor(),          # Convert images to tensors
    ])

    # Create dataset and dataloader
    if datasetloader.lower() == "local":
        dataset = DatasetLoader(metadata_file=metadata_file, root_dir=root_dir, transform=transform) 
        print(f"Dataset length: {len(dataset)}")
    elif datasetloader.lower() == "internet":
        dataset = DatasetLoaderfromInternet(metadata_url=metadata_file, root_url=root_dir, transform=transform)
        print(f"Dataset length: {len(dataset)}")
    else:
        print(f"Cannot find the specified dataset loader `{datasetloader}` from local and internet.\nPlease check properly.")
        raise SystemError

    # Load one image to test
    try:
        sample_img = dataset[0]
        print(f"Sample image size: {sample_img.size()}")
    except FileNotFoundError as e:
        print(e)
        return

    # Create DataLoader and Iterate
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Visualize Sample Images
    # Get a batch of training data
    for i, batch in enumerate(dataloader):
        if i == 0:  # Only visualize the first batch
            images = batch
            break

    # Make a grid from batch
    out = vutils.make_grid(images, padding=2, normalize=True)

    # Plot the grid
    plt.figure(figsize=(12, 12))
    plt.imshow(out.permute(1, 2, 0))
    plt.title('Batch of Images')
    #plt.show()

    # Check for GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Initialize the models
    discriminator = Discriminator().to(device)

    if model.lower() == "usrgan":
        generator = USRGAN().to(device)
    elif model.lower() == "esrgan":
        generator = ESRGAN().to(device)
    elif model.lower() == "bsrgan":
        generator = BSRGAN().to(device)
    elif model.lower() == "isrgan":
        generator = ISRGAN().to(device)
    elif model.lower() == "rsrgan":
        generator = RSRGAN().to(device)
    elif model.lower() == "srgan":
        generator = SRGAN().to(device)
    else:
        print(f"Cannot find the specified network `{model}` from usrgan, esrgan, bsrgan, isrgan, rsrgan and srgan.\nPlease check properly.")
        raise SystemError

    print("Initialized the models")

    # Define loss and optimizers
    criterion = nn.BCELoss()
    optimizer_d = optim.Adam(discriminator.parameters(), lr=0.0002, betas=(0.5, 0.999))
    optimizer_g = optim.Adam(generator.parameters(), lr=0.0002, betas=(0.5, 0.999))
    print("Defined loss and optimizers")

    name = input("What would you like to call your model?: ")

    # Create directory for saving models
    os.makedirs("out_models", exist_ok=True)

    # Training the GAN
    print("Training Started")

    for epoch in range(epochs):
        for i, data in enumerate(dataloader):
            real_images = data.to(device)
            batch_size = real_images.size(0)

            # Labels for real and fake images
            real_labels = torch.ones(batch_size, 1).to(device)
            fake_labels = torch.zeros(batch_size, 1).to(device)

            # Train the discriminator with real images
            discriminator.zero_grad()
            outputs = discriminator(real_images)
            d_loss_real = criterion(outputs, real_labels)
            real_score = outputs

            # Generate fake images
            noise = torch.randn(batch_size, 3, 256, 256).to(device)
            fake_images = generator(noise)
            outputs = discriminator(fake_images.detach())
            d_loss_fake = criterion(outputs, fake_labels)
            fake_score = outputs

            # Backprop and optimize the discriminator
            d_loss = d_loss_real + d_loss_fake
            d_loss.backward()
            optimizer_d.step()

            # Train the generator
            generator.zero_grad()
            outputs = discriminator(fake_images)
            g_loss = criterion(outputs, real_labels)

            # Backprop and optimize the generator
            g_loss.backward()
            optimizer_g.step()

            if (i+1) % 200 == 0:
                print(f'Epoch [{epoch+1}/{epochs}], Step [{i+1}/{len(dataloader)}], '
                      f'D Loss: {d_loss.item():.4f}, G Loss: {g_loss.item():.4f}, '
                      f'D(x): {real_score.mean().item():.4f}, D(G(z)): {fake_score.mean().item():.4f}')

        # Save the model checkpoints after each epoch
        torch.save(generator.state_dict(), os.path.join("models", f"{name}_G_{epoch+1}.pnn"))
        torch.save(discriminator.state_dict(), os.path.join("models", f"{name}_D_{epoch+1}.pnn"))
        print(f"Model checkpoints saved for epoch {epoch+1}")

    # Save the final models
    torch.save(generator.state_dict(), os.path.join("models", f"{name}_Generator.pnn"))
    torch.save(discriminator.state_dict(), os.path.join("models", f"{name}_Discriminator.pnn"))
    print(f"Model saved at {os.path.abspath(name)}_Generator.pnn, "
          f"Model saved at {os.path.abspath(name)}_Discriminator.pnn")
